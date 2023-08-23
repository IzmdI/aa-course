import enum

from sqlalchemy import BigInteger, Column, Enum, String, Uuid

from analytics.src.db.tables import BaseModel
from analytics.src.db.declarative import SCHEMA


class TransactionType(str, enum.Enum):
    TASK = "task"
    PAYMENT = "payment"


class BillingCycle(BaseModel):
    __tablename__ = "billing_cycle"

    public_id = Column(Uuid, nullable=False, unique=True)
    total_income = Column(BigInteger, nullable=False)


class BillingTransaction(BaseModel):
    __tablename__ = "billing_transactions"

    public_id = Column(Uuid, nullable=False, unique=True)
    user_id = Column(Uuid, nullable=False)
    credit = Column(BigInteger, nullable=False)
    debit = Column(BigInteger, nullable=False)
    description = Column(String, nullable=False)
    type = Column(Enum(TransactionType, schema=SCHEMA), nullable=False)
