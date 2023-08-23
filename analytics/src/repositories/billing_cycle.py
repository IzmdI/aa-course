import datetime
from uuid import UUID

from sqlalchemy import Date, cast, delete, desc, select, update
from sqlalchemy.exc import IntegrityError

from analytics.src.db.tables import BillingCycle
from analytics.src.repositories.repo_base import BaseRepository


class BillingCycleRepo(BaseRepository):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(BillingCycle.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_cycle_by_id(self, cycle_id: int) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(id=cycle_id)
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def get_cycle(self, date: datetime.date | None = None, **kwargs) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(**kwargs).order_by(desc(BillingCycle.updated_at))
        if date:
            query = query.filter(cast(BillingCycle.updated_at, Date) == date)
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def get_cycle_by_public_id(self, public_id: int) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(public_id=public_id)
        cycle = await self.session.execute(query)
        return cycle.scalar_one_or_none()

    async def get_current_billing_cycle(self) -> BillingCycle | None:
        query = select(BillingCycle).filter_by(is_active=True).order_by(desc(BillingCycle.updated_at))
        cycle = await self.session.execute(query)
        return cycle.scalars().first()

    async def create_cycle(self, **kwargs) -> BillingCycle:
        cycle = BillingCycle(**kwargs)
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
