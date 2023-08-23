from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette import status
from typing_extensions import AsyncGenerator

from auth.src.application.settings.auth import Settings as Auth_settings
from auth.src.controllers.stub import Stub
from auth.src.db.tables import User, UserRole
from auth.src.dto.user import TokenPayload
from auth.src.repositories.user import UserRepo
from auth.src.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(user_repo=UserRepo(session), pwd_context=pwd_context)


async def get_current_user(
    service: UserService = Depends(get_user_service),
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


def get_current_moderator_user(
    user: User = Depends(get_current_active_user),
) -> User:
    if user.role not in (UserRole.ADMIN.value, UserRole.MODERATOR.value):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user
