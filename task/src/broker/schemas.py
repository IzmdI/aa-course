from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from task.src.db.tables import Task, TaskStatus, User, UserRole


class Action(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class ProducerEvent(BaseModel):
    topic: str
    value: str | dict[str, Any]
    key: UUID = uuid4()


class ConsumerEvent(BaseModel):
    topic: str
    value: str | dict[str, Any]
    key: UUID = uuid4()


class EventData(BaseModel):
    event_id: UUID = uuid4()
    event_version: int = 1
    event_name: str
    event_time: str = datetime.now().isoformat(timespec="milliseconds")
    event_producer: str
    event_data: dict


class UserStreamingData(BaseModel):
    action: Action
    public_id: UUID
    username: Optional[str] = None
    role: Optional[UserRole] = None
    email: Optional[str] = None

    @classmethod
    def from_model(cls, model: User, action: Action):
        return cls(
            action=action, public_id=model.public_id, role=model.role, username=model.username, email=model.email
        )


class UserRoleData(BaseModel):
    action: Action
    public_id: UUID
    role: UserRole

    @classmethod
    def from_model(cls, model: User, action: Action):
        return cls(action=action, public_id=model.public_id, role=model.role)


class EventDataUserStreaming(EventData):
    event_data: UserStreamingData


class EventDataUserRole(EventData):
    event_data: UserRoleData


class TaskStreamingData(BaseModel):
    action: Action
    title: str
    public_id: UUID
    price: int
    description: Optional[str] = None
    assignee_id: UUID

    @classmethod
    def from_model(cls, model: Task, action: Action):
        return cls(
            action=action,
            title=model.title,
            public_id=model.public_id,
            price=model.price,
            description=model.description,
            assignee_id=model.assignee_id,
        )


class TaskDoneData(BaseModel):
    action: Action
    public_id: UUID
    assignee_id: UUID
    fee: int

    @classmethod
    def from_model(cls, model: Task, action: Action):
        return cls(action=action, public_id=model.public_id, assignee_id=model.assignee_id, fee=model.fee)


class EventDataTaskStreaming(EventData):
    event_data: TaskStreamingData


class EventDataTaskDone(EventData):
    event_data: TaskDoneData
