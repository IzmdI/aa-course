import datetime
from typing import Optional
from uuid import UUID

from billing.src.dto.base import BaseSchema


class TransactionCreateDTO(BaseSchema):
    user_id: UUID
    credit: Optional[int] = None
    debit: Optional[int] = None
    description: str
    billing_cycle_id: UUID
