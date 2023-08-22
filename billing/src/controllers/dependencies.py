from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette import status
from typing_extensions import AsyncGenerator

from billing.src.application.settings.auth import Settings as Auth_settings
from billing.src.controllers.stub import Stub
from billing.src.db.tables import User, UserRole
from billing.src.dto.user import TokenPayload
from billing.src.repositories.user import UserRepo
from billing.src.repositories.billing_transaction import BillingTransactionRepo
from billing.src.repositories.billing_cycle import BillingCycleRepo
from billing.src.services.billing import BillingService

# TODO: брать адрес из env / настроек
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8010/api/v1/token")


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


async def get_billing_service(session: AsyncSession = Depends(get_session)) -> BillingService:
    return BillingService(
        user_repo=UserRepo(session),
        transactions_repo=BillingTransactionRepo(session),
        cycle_repo=BillingCycleRepo(session),
    )


async def get_current_user(
    service: BillingService = Depends(get_billing_service),
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


def get_current_accountant_user(
    user: User = Depends(get_current_active_user),
) -> User:
    if user.role not in (UserRole.ADMIN, UserRole.ACCOUNTANT):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user
