from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette import status
from typing_extensions import AsyncGenerator

from analytics.src.application.settings.auth import Settings as Auth_settings
from analytics.src.controllers.stub import Stub
from analytics.src.db.tables import User, UserRole
from analytics.src.dto.user import TokenPayload
from analytics.src.repositories.user import UserRepo
from analytics.src.repositories.task import TaskRepo
from analytics.src.repositories.billing_transaction import BillingTransactionRepo
from analytics.src.repositories.billing_cycle import BillingCycleRepo
from analytics.src.services.analytics import AnalyticsService

# TODO: брать адрес из env / настроек
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8010/api/v1/token")


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


async def get_analytics_service(session: AsyncSession = Depends(get_session)) -> AnalyticsService:
    return AnalyticsService(
        user_repo=UserRepo(session),
        task_repo=TaskRepo(session),
        transactions_repo=BillingTransactionRepo(session),
        cycle_repo=BillingCycleRepo(session),
    )


async def get_current_user(
    service: AnalyticsService = Depends(get_analytics_service),
    auth_settings: Auth_settings = Depends(Stub(Auth_settings)),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await service.user_repo.get_user(username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_admin_user(
    user: User = Depends(get_current_active_user),
) -> User:
    if user.role not in (UserRole.ADMIN,):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user
