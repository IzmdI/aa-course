from uuid import UUID

from db.tables import TaskStatus
from dto.base import BaseSchema, ORMBaseSchema


class TaskDTO(ORMBaseSchema):
    public_id: UUID
    price: int
    fee: int
    text: str
    owner_id: UUID
    assignee_id: UUID
    status: TaskStatus


class TaskCreateDTO(BaseSchema):
    price: int | None
    fee: int | None
    text: str
    owner_id: UUID | None
    assignee_id: UUID | None
    status: TaskStatus = TaskStatus.ASSIGNED
