import datetime
from typing import Any, Sequence

from sqlalchemy import Date, Row, RowMapping, cast, select
from sqlalchemy.exc import IntegrityError

from analytics.src.db.tables import BillingTransaction
from analytics.src.dto.billing import TransactionCreateDTO
from analytics.src.repositories.repo_base import BaseRepository


class BillingTransactionRepo(BaseRepository):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(BillingTransaction.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_transaction_by_id(self, transaction_id: int) -> BillingTransaction | None:
        query = select(BillingTransaction).filter_by(id=transaction_id)
        transaction = await self.session.execute(query)
        return transaction.scalar_one_or_none()

    async def get_transaction_by_public_id(self, public_id: int) -> BillingTransaction | None:
        query = select(BillingTransaction).filter_by(public_id=public_id)
        transaction = await self.session.execute(query)
        return transaction.scalar_one_or_none()

    async def get_transactions(
        self, date: datetime.date | None = None, **kwargs
    ) -> list[BillingTransaction] | Sequence[Row | RowMapping | Any]:
        query = select(BillingTransaction).filter_by(**kwargs)
        if date:
            query = query.filter(cast(BillingTransaction.updated_at, Date) == date)
        transactions = await self.session.execute(query)
        return transactions.scalars().all()

    async def create_transaction(self, transaction_data: TransactionCreateDTO) -> BillingTransaction:
        transaction = BillingTransaction(**transaction_data.model_dump(exclude_none=True))
        unique_fields_exceptions = await self.validate_uniques(transaction)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(transaction)
        await self.session.flush([transaction])
        return transaction

    async def bulk_create_transactions(self, transactions_data: list[TransactionCreateDTO]) -> None:
        transactions = [BillingTransaction(**data.model_dump(exclude_none=True)) for data in transactions_data]
        self.session.add_all(transactions)
        await self.session.flush(transactions)
