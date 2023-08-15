from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field

from db.tables import TaskStatus


class OrderingType(str, Enum):
    asc = "asc"
    desc = "desc"


class OrderingFieldBase(str, Enum):
    id = "id"
    created_at = "created_at"
    updated_at = "updated_at"


class CommonBaseQueryParamSchema(BaseModel):
    offset: int | None = Field(Query(None, ge=0, le=1000, example=0, description="смещение"))
    limit: int | None = Field(Query(None, gt=0, le=1000, example=100, description="лимит"))
    order_by: OrderingFieldBase | None = OrderingFieldBase.id
    ordering: OrderingType = OrderingType.asc
    is_active: bool | None = Field(Query(True, example=True, description="признак логического удаления"))


class TaskFilterSchema(BaseModel):
    task_id: int | None = None
    price: int | None = None
    fee: int | None = None
    text: str | None = None
    owner_id: int | None = None
    assignee_id: int | None = None
    status: TaskStatus | None = None
