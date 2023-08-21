import datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from billing.src.db.tables import BillingCycle
from billing.src.repositories.repo_base import BaseRepository


class BillingCycleRepo(BaseRepository):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(BillingCycle.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_cycle_by_id(self, cycle_id: int) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(id=cycle_id)
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def get_cycle_by_public_id(self, public_id: int) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(public_id=public_id)
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def get_current_billing_cycle(self) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(date=datetime.date.today())
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def create_cycle(self) -> BillingCycle:
        cycle = BillingCycle()
        unique_fields_exceptions = await self.validate_uniques(cycle)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(cycle)
        await self.session.flush([cycle])
        return cycle

    async def update_cycle(self, public_id: UUID, **kwargs) -> None:
        try:
            query = update(BillingCycle).values(**kwargs).filter_by(public_id=public_id)
            await self.session.execute(query)
        except IntegrityError:
            unique_fields_exceptions = await self.validate_uniques_by_values(BillingCycle, kwargs)
            if unique_fields_exceptions:
                raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)

    async def delete_cycle_by_public_id(self, public_id: UUID) -> None:
        query = delete(BillingCycle).filter_by(public_id=public_id)
        await self.session.execute(query)
