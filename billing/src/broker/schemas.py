from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from billing.src.db.tables import UserRole


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
    balance: Optional[int] = None


class UserRoleData(BaseModel):
    action: Action
    public_id: UUID
    role: UserRole


class EventDataUserStreaming(EventData):
    event_data: UserStreamingData


class EventDataUserRole(EventData):
    event_data: UserRoleData


class TaskStreamingData(BaseModel):
    action: Action
    title: str
    jira_id: Optional[str] = None
    public_id: UUID
    price: int
    description: Optional[str] = None
    assignee_id: UUID


class TaskDoneData(BaseModel):
    action: Action
    public_id: UUID
    assignee_id: UUID
    fee: int


class EventDataTaskStreaming(EventData):
    event_data: TaskStreamingData


class EventDataTaskDone(EventData):
    event_data: TaskDoneData
