import datetime
from typing import Optional
from uuid import UUID

from billing.src.dto.base import BaseSchema, ORMBaseSchema
from billing.src.db.tables.billing import TransactionType


class TransactionCreateDTO(BaseSchema):
    user_id: UUID
    credit: Optional[int] = 0
    debit: Optional[int] = 0
    description: str
    billing_cycle_id: UUID
    type: Optional[TransactionType] = TransactionType.TASK


class TransactionResponseDTO(ORMBaseSchema):
    credit: int
    debit: int
    description: str
    type: TransactionType


class TotalIncomeResponse(BaseSchema):
    date: datetime.date = datetime.date.today()
    total_income: int = 0


class UserReportResponse(BaseSchema):
    user_id: UUID
    user_balance: int
    user_auditlog: list[TransactionResponseDTO]
