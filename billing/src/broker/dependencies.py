from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from billing.src.application.settings.broker import Settings as Broker_settings
from billing.src.application.settings.db import Settings as DB_settings
from billing.src.broker.service import BrokerUserService, BrokerBillingService

db_url = DB_settings().get_db_url()
billing_engine = create_async_engine(db_url)
sessionmaker_class = async_sessionmaker(billing_engine, expire_on_commit=False)
broker_settings = Broker_settings()


async def get_session(sessionmaker: async_sessionmaker = sessionmaker_class) -> AsyncGenerator:
    async with sessionmaker() as session_obj:
        yield session_obj


async def get_user_broker_service() -> BrokerUserService:
    session: AsyncSession = await anext(get_session())
    return BrokerUserService(session)


async def get_billing_broker_service() -> BrokerBillingService:
    session: AsyncSession = await anext(get_session())
    return BrokerBillingService(session)
