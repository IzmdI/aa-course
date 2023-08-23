import datetime
from typing import Optional
from uuid import UUID

from analytics.src.dto.base import BaseSchema, ORMBaseSchema
from analytics.src.db.tables.billing import TransactionType
from analytics.src.dto.task import TaskDTO


class BillingCycleCreateDTO(BaseSchema):
    public_id: UUID
    total_income: int


class BillingCycleUpdateDTO(BaseSchema):
    total_income: Optional[int] = None


class TransactionCreateDTO(BaseSchema):
    user_id: UUID
    credit: int
    debit: int
    description: str
    billing_cycle_id: UUID
    type: TransactionType


class TotalIncomeResponse(BaseSchema):
    date: datetime.date = datetime.date.today()
    total_income: int = 0


class TaskRatingResponse(BaseSchema):
    today_top: TaskDTO
    week_top: TaskDTO
    month_top: TaskDTO
