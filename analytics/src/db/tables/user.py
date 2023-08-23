import enum

from sqlalchemy import BigInteger, Column, Enum, String, Uuid

from analytics.src.db.declarative import SCHEMA
from analytics.src.db.tables import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    ACCOUNTANT = "accountant"
    WORKER = "worker"


class User(BaseModel):
    __tablename__ = "users"

    public_id = Column(Uuid, nullable=False, unique=True)
    username = Column(String(32), nullable=True, unique=True)
    role = Column(Enum(UserRole, schema=SCHEMA), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    balance = Column(BigInteger, nullable=False, default=0)
