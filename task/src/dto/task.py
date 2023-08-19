from uuid import UUID

from db.tables import TaskStatus
from dto.base import BaseSchema, ORMBaseSchema


class TaskDTO(ORMBaseSchema):
    title: str
    public_id: UUID
    price: int
    fee: int
    description: str | None
    owner_id: UUID
    assignee_id: UUID
    status: TaskStatus


class TaskCreateDTO(BaseSchema):
    title: str
    price: int | None
    fee: int | None
    description: str | None
    owner_id: UUID | None
    assignee_id: UUID | None
    status: TaskStatus = TaskStatus.ASSIGNED
