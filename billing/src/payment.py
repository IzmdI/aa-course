import asyncio
import sys
from typing import AsyncGenerator

from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from billing.src.services.billing import BillingService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from billing.src.application.settings.db import Settings as DB_settings
from billing.src.dto.billing import TransactionCreateDTO
from billing.src.db.tables.billing import TransactionType
from billing.src.repositories.billing_transaction import BillingTransactionRepo

from billing.src.repositories.billing_cycle import BillingCycleRepo
from billing.src.repositories.user import UserRepo

db_url = DB_settings().get_db_url()
billing_engine = create_async_engine(db_url)
sessionmaker_class = async_sessionmaker(billing_engine, expire_on_commit=False)


async def get_session(sessionmaker: async_sessionmaker = sessionmaker_class) -> AsyncGenerator:
    # TODO: разобраться с GeneratorExit при повторном вызове сессии
    async with sessionmaker() as session_obj:
        yield session_obj


async def get_billing_service() -> BillingService:
    session: AsyncSession = await anext(get_session())
    return BillingService(
        user_repo=UserRepo(session),
        transactions_repo=BillingTransactionRepo(session),
        cycle_repo=BillingCycleRepo(session),
    )


async def payment() -> None:
    service = await get_billing_service()
    current_cycle = await service.cycle_repo.get_current_billing_cycle()
    if not current_cycle:
        return
    current_cycle.is_active = False
    await service.cycle_repo.session.commit()
    users = await service.user_repo.get_users_with_positive_balance()
    transactions = []
    for user in users:
        transactions.append(
            TransactionCreateDTO(
                billing_cycle_id=current_cycle.public_id,
                user_id=user.public_id,
                description="Popug earned some mooooooney!",
                credit=user.balance,
                type=TransactionType.PAYMENT,
            )
        )
        user.balance = 0
        # TODO: логика выплаты и уведомления о выплате
    await service.transactions_repo.bulk_create_transactions(transactions)
    await service.transactions_repo.session.commit()


if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=payment,
        trigger="cron",
        minute="0",
        hour="21",
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (SchedulerAlreadyRunningError, RuntimeError, SystemExit, KeyboardInterrupt):
        pass
