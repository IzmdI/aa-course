import enum

from sqlalchemy import BigInteger, Column, Enum, Integer, String

from db.declarative import SCHEMA
from db.tables import BaseModel


class TaskStatus(str, enum.Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    DONE = "done"


class Task(BaseModel):
    __tablename__ = "tasks"

    price = Column(Integer, nullable=False)
    fee = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    assignee_id = Column(BigInteger, nullable=False)
    status = Column(Enum(TaskStatus, schema=SCHEMA), nullable=False, default=TaskStatus.NEW)
