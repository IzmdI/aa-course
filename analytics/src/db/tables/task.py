import enum

from sqlalchemy import Column, Enum, Integer, String, Uuid

from analytics.src.db.declarative import SCHEMA
from analytics.src.db.tables import BaseModel


class TaskStatus(str, enum.Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    DONE = "done"


class Task(BaseModel):
    __tablename__ = "tasks"

    title = Column(String(320), nullable=False)
    jira_id = Column(String(320), nullable=True)
    public_id = Column(Uuid, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    fee = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Uuid, nullable=False)
    assignee_id = Column(Uuid, nullable=False)
    status = Column(Enum(TaskStatus, schema=SCHEMA), nullable=False)
