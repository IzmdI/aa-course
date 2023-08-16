import enum
from uuid import uuid4

from sqlalchemy import Column, Enum, Integer, String, Uuid

from db.declarative import SCHEMA
from db.tables import BaseModel


class TaskStatus(str, enum.Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    DONE = "done"


class Task(BaseModel):
    __tablename__ = "tasks"

    public_id = Column(Uuid, nullable=False, unique=True, default=uuid4)
    price = Column(Integer, nullable=False)
    fee = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    owner_id = Column(Uuid, nullable=False)
    assignee_id = Column(Uuid, nullable=False)
    status = Column(Enum(TaskStatus, schema=SCHEMA), nullable=False, default=TaskStatus.NEW)
