import enum

from sqlalchemy import BigInteger, Column, Enum, String

from db.declarative import SCHEMA
from db.tables import BaseModel


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    ACCOUNTANT = "accountant"
    WORKER = "worker"


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(Enum(UserRole, schema=SCHEMA), nullable=False, default=UserRole.WORKER)
    bill = Column(BigInteger, nullable=False, unique=True)
