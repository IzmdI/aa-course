from typing import Optional
from uuid import UUID

from analytics.src.db.tables import TaskStatus
from analytics.src.dto.base import BaseSchema, ORMBaseSchema


class TaskDTO(ORMBaseSchema):
    title: str
    jira_id: Optional[str] = None
    public_id: UUID
    price: int
    fee: int
    description: Optional[str] = None
    owner_id: UUID
    assignee_id: UUID
    status: TaskStatus


class TaskCreateDTO(BaseSchema):
    title: str
    jira_id: Optional[str] = None
    price: Optional[int] = None
    fee: Optional[int] = None
    description: Optional[str] = None
    owner_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    status: Optional[TaskStatus] = TaskStatus.ASSIGNED


class TaskUpdateDTO(BaseSchema):
    title: Optional[str] = None
    jira_id: Optional[str] = None
    price: Optional[int] = None
    fee: Optional[int] = None
    description: Optional[str] = None
    owner_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    status: Optional[TaskStatus] = None
