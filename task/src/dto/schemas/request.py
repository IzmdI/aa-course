from enum import Enum
from typing import Optional
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
    offset: Optional[int] = Field(Query(None, ge=0, le=1000, example=0, description="смещение"))
    limit: Optional[int] = Field(Query(None, gt=0, le=1000, example=100, description="лимит"))
    order_by: Optional[OrderingFieldBase] = OrderingFieldBase.id
    ordering: Optional[OrderingType] = OrderingType.asc
    is_active: Optional[bool] = Field(Query(True, example=True, description="признак логического удаления"))


class TaskFilterSchema(BaseModel):
    task_id: Optional[int] = Field(Query(None, gt=0, description="идентификатор задачи"))
    price: Optional[int] = Field(Query(None, ge=10, le=20, description="цена задачи"))
    fee: Optional[int] = Field(Query(None, ge=20, le=40, description="вознаграждение задачи"))
    text: Optional[str] = Field(Query(None, description="описание задачи"))
    owner_id: Optional[UUID] = Field(Query(None, description="публичный идентификатор постановщика задачи"))
    assignee_id: Optional[UUID] = Field(Query(None, description="публичный идентификатор исполнителя задачи"))
    status: Optional[TaskStatus] = Field(Query(None, description="статус задачи"))
