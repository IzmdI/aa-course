from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from billing.src.db.tables import BillingTransaction
from billing.src.dto.billing import TransactionCreateDTO
from billing.src.repositories.repo_base import BaseRepository


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

    async def create_transaction(self, transaction_data: TransactionCreateDTO) -> BillingTransaction:
        transaction = BillingTransaction(**transaction_data.model_dump(exclude_none=True))
        unique_fields_exceptions = await self.validate_uniques(transaction)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(transaction)
        await self.session.flush([transaction])
        return transaction

    # обновление транзакионных записей не предполагается
    # async def update_transaction(self, public_id: UUID, **kwargs) -> None:
    #     try:
    #         query = update(BillingTransaction).values(**kwargs).filter_by(public_id=public_id)
    #         await self.session.execute(query)
    #     except IntegrityError:
    #         unique_fields_exceptions = await self.validate_uniques_by_values(BillingTransaction, kwargs)
    #         if unique_fields_exceptions:
    #             raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)

    # удаление транзакионных записей не предполагается
    # async def delete_transaction_by_public_id(self, public_id: UUID) -> None:
    #     query = delete(BillingTransaction).filter_by(public_id=public_id)
    #     await self.session.execute(query)
