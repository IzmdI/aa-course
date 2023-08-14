from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing_extensions import AsyncGenerator

from controllers.stub import Stub
from repositories.user import UserRepo
from services.user import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(user_repo=UserRepo(session), pwd_context=pwd_context)
