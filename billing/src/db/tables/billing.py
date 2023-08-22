import enum
from uuid import uuid4

from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from billing.src.db.tables import BaseModel
from billing.src.db.declarative import SCHEMA


class TransactionType(str, enum.Enum):
    TASK = "task"
    PAYMENT = "payment"


class BillingCycle(BaseModel):
    __tablename__ = "billing_cycle"

    public_id = Column(Uuid, nullable=False, unique=True, default=uuid4)
    total_income = Column(BigInteger, nullable=False, default=0)

    transactions = relationship("BillingTransaction", back_populates="billing_cycle", lazy="noload")


class BillingTransaction(BaseModel):
    __tablename__ = "billing_transactions"

    public_id = Column(Uuid, nullable=False, unique=True, default=uuid4)
    user_id = Column(Uuid, nullable=False)
    credit = Column(BigInteger, nullable=False, default=0)
    debit = Column(BigInteger, nullable=False, default=0)
    description = Column(String, nullable=False)
    type = Column(Enum(TransactionType, schema=SCHEMA), nullable=False, default=TransactionType.TASK)

    billing_cycle_id = Column(Uuid, ForeignKey("billing_cycle.public_id"), nullable=False)
    billing_cycle = relationship("BillingCycle", back_populates="transactions", lazy="noload", uselist=False)
