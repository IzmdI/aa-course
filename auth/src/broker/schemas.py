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
