from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing_extensions import AsyncGenerator

from controllers.stub import Stub


async def get_session(sessionmaker: async_sessionmaker = Depends(Stub(async_sessionmaker))) -> AsyncGenerator:
    async with sessionmaker() as session:
        yield session
