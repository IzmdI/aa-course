from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette import status
from typing_extensions import AsyncGenerator

from task.src.application.settings.auth import Settings as Auth_settings
from task.src.controllers.stub import Stub
from task.src.db.tables import User, UserRole
from task.src.dto.user import TokenPayload
from task.src.repositories.task import TaskRepo
from task.src.repositories.user import UserRepo
from task.src.services.task import TaskService

# TODO: брать адрес из env / настроек
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8010/api/v1/token")


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


async def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    return TaskService(user_repo=UserRepo(session), task_repo=TaskRepo(session))


async def get_current_user(
    service: TaskService = Depends(get_task_service),
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
