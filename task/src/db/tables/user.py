import enum

from sqlalchemy import Column, Enum, String, Uuid

from db.declarative import SCHEMA
from db.tables import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    ACCOUNTANT = "accountant"
    WORKER = "worker"


class User(BaseModel):
    __tablename__ = "users"

    public_id = Column(Uuid, nullable=False, unique=True)
    username = Column(String(32), nullable=True, unique=True)
    role = Column(Enum(UserRole, schema=SCHEMA), nullable=False, default=UserRole.WORKER)
    email = Column(String(255), nullable=True, unique=True)
