from db.tables import TaskStatus
from dto.base import BaseSchema, ORMBaseSchema


class TaskDTO(ORMBaseSchema):
    price: int
    fee: int
    text: str
    owner_id: int
    assignee_id: int
    status: TaskStatus


class TaskCreateDTO(BaseSchema):
    price: int | None
    fee: int | None
    text: str
    owner_id: int | None
    assignee_id: int | None
    status: TaskStatus = TaskStatus.ASSIGNED
