from enum import Enum
from uuid import UUID

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
    task_id: int | None = Field(Query(None, gt=0, description="идентификатор задачи"))
    price: int | None = Field(Query(None, ge=10, le=20, description="цена задачи"))
    fee: int | None = Field(Query(None, ge=20, le=40, description="вознаграждение задачи"))
    text: str | None = Field(Query(None, description="описание задачи"))
    owner_id: UUID | None = Field(Query(None, description="публичный идентификатор постановщика задачи"))
    assignee_id: UUID | None = Field(Query(None, description="публичный идентификатор исполнителя задачи"))
    status: TaskStatus | None = Field(Query(None, description="статус задачи"))
