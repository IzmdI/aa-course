from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from db.tables import User, UserRole


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
