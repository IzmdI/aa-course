import datetime
from uuid import uuid4

from sqlalchemy import BigInteger, Column, Date, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from billing.src.db.tables import BaseModel


class BillingCycle(BaseModel):
    __tablename__ = "billing_cycle"

    public_id = Column(Uuid, nullable=False, unique=True, default=uuid4)
    date = Column(Date, nullable=False, default=datetime.date.today)

    transactions = relationship("BillingTransaction", back_populates="billing_cycle", lazy="noload")


class BillingTransaction(BaseModel):
    __tablename__ = "billing_transactions"

    public_id = Column(Uuid, nullable=False, unique=True, default=uuid4)
    user_id = Column(Uuid, nullable=False)
    credit = Column(BigInteger, nullable=False, default=0)
    debit = Column(BigInteger, nullable=False, default=0)
    description = Column(String, nullable=False)

    billing_cycle_id = Column(Uuid, ForeignKey("billing_cycle.public_id"), nullable=False)
    billing_cycle = relationship("BillingCycle", back_populates="transactions", lazy="noload", uselist=False)
