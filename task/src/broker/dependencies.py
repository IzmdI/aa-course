from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from application.settings.db import Settings as DB_settings
from application.settings.broker import Settings as Broker_settings
from broker.service import BrokerUserService

db_url = DB_settings().get_db_url()
engine = create_async_engine(db_url)
sessionmaker_class = async_sessionmaker(engine, expire_on_commit=False)
broker_settings = Broker_settings()


async def get_session(sessionmaker: async_sessionmaker = sessionmaker_class) -> AsyncGenerator:
    async with sessionmaker() as session_obj:
        yield session_obj


async def get_broker_service() -> BrokerUserService:
    session: AsyncSession = await anext(get_session())
    return BrokerUserService(session)
