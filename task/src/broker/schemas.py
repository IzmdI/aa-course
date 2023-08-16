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
    key: UUID = uuid4()

    @staticmethod
    def dict_factory_for_batch(item: dict):
        exclude_fields = ("topic",)
        return {key: value for key, value in item if key not in exclude_fields}


@dataclass
class ConsumerEvent:
    topic: str
    value: str | dict[str, Any]
    key: UUID = uuid4()


@dataclass
class UserMessage:
    action: Action
    public_id: UUID
    username: str
    role: UserRole
    email: str | None

    @classmethod
    def from_model(cls, model: User, action: Action):
        return cls(
            action=action,
            public_id=model.public_id,
            role=model.role,
            username=model.username,
            email=model.email,
        )


@dataclass
class TaskMessage:
    action: Action
    public_id: UUID
    price: int
    fee: int
    text: str
    owner_id: UUID
    assignee_id: UUID
    status: TaskStatus

    @classmethod
    def from_model(cls, model: Task, action: Action):
        return cls(
            action=action,
            public_id=model.public_id,
            price=model.price,
            fee=model.fee,
            text=model.text,
            owner_id=model.owner_id,
            assignee_id=model.assignee_id,
            status=model.status,
        )
