from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from db.tables import Task, TaskStatus, User, UserRole


class Action(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


@dataclass
class ProducerEvent:
    topic: str
    value: str | dict[str, Any]
    key: str | int | UUID = uuid4()


@dataclass
class ConsumerEvent:
    topic: str
    value: str | dict[str, Any]
    key: str | int | UUID = uuid4()


@dataclass
class UserMessage:
    action: Action
    sso_id: int
    username: str
    role: UserRole
    email: str | None

    @classmethod
    def from_model(cls, model: User, action: Action):
        return cls(action=action, sso_id=model.id, role=model.role, username=model.username, email=model.email)


@dataclass
class TaskMessage:
    action: Action
    task_id: int
    price: int
    fee: int
    text: str
    owner_id: int
    assignee_id: int
    status: TaskStatus

    @classmethod
    def from_model(cls, model: Task, action: Action):
        return cls(
            action=action,
            task_id=model.id,
            price=model.price,
            fee=model.fee,
            text=model.text,
            owner_id=model.owner_id,
            assignee_id=model.assignee_id,
            status=model.status,
        )
