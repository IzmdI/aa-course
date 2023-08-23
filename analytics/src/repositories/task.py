import datetime
from typing import Any, Literal, Sequence
from uuid import UUID

from sqlalchemy import Date, Row, RowMapping, and_, cast, delete, extract, select, update, desc
from sqlalchemy.exc import IntegrityError

from analytics.src.db.tables import Task, TaskStatus
from analytics.src.dto.schemas.request import CommonBaseQueryParamSchema
from analytics.src.dto.task import TaskCreateDTO
from analytics.src.repositories.const import SortingType
from analytics.src.repositories.repo_base import BaseRepository


class TaskRepo(BaseRepository):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(Task.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_task_by_id(self, task_id: int, by_undone_status: bool = False) -> Task | None:
        query = select(Task).filter_by(id=task_id)
        if by_undone_status:
            query = query.filter(Task.status != TaskStatus.DONE)
        task = await self.session.execute(query)
        return task.scalar_one_or_none()

    async def get_top_task(self, period: Literal["today", "week", "month"]) -> Task | None:
        today = datetime.date.today()
        query = select(Task).filter_by(status=TaskStatus.DONE)
        match period:
            case "today":
                query = query.filter(cast(Task.updated_at, Date) == today)
            case "week":
                query = query.filter(
                    and_(cast(Task.updated_at, Date) <= today),
                    cast(Task.updated_at, Date) >= today - datetime.timedelta(weeks=1.0),
                )
            case "month":
                query = query.filter(extract("month", cast(Task.updated_at, Date)) == today.month)
        query = query.order_by(desc(Task.fee))
        task = await self.session.execute(query)
        return task.scalars().first()

    async def get_tasks(
        self, common_params: CommonBaseQueryParamSchema, **kwargs
    ) -> list[Task] | Sequence[Row | RowMapping | Any]:
        query = (
            select(Task)
            .filter_by(is_active=common_params.is_active, **kwargs)
            .limit(common_params.limit)
            .offset(common_params.offset)
        )
        if common_params.order_by:
            query = query.order_by(getattr(SortingType, common_params.ordering)(common_params.order_by))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_task(self, task_data: TaskCreateDTO) -> Task:
        task = Task(**task_data.model_dump(exclude_none=True))
        unique_fields_exceptions = await self.validate_uniques(task)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(task)
        await self.session.flush([task])
        return task

    async def update_task(self, public_id: UUID, **kwargs) -> None:
        try:
            query = update(Task).values(**kwargs).filter_by(public_id=public_id)
            await self.session.execute(query)
        except IntegrityError:
            unique_fields_exceptions = await self.validate_uniques_by_values(Task, kwargs)
            if unique_fields_exceptions:
                raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)

    async def delete_task(self, task_id: int) -> None:
        query = delete(Task).filter_by(id=task_id)
        await self.session.execute(query)

    async def delete_task_by_public_id(self, public_id: UUID) -> None:
        query = delete(Task).filter_by(public_id=public_id)
        await self.session.execute(query)
