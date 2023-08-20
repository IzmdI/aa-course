from typing import Optional
from uuid import UUID

from db.tables import TaskStatus
from dto.base import BaseSchema, ORMBaseSchema


class TaskDTO(ORMBaseSchema):
    title: str
    public_id: UUID
    price: int
    fee: int
    description: Optional[str] = None
    owner_id: UUID
    assignee_id: UUID
    status: TaskStatus


class TaskCreateDTO(BaseSchema):
    title: str
    price: Optional[int] = None
    fee: Optional[int] = None
    description: Optional[str] = None
    owner_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    status: Optional[TaskStatus] = TaskStatus.ASSIGNED
