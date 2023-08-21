from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


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
