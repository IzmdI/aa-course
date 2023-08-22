import datetime

from billing.src.repositories.billing_transaction import BillingTransactionRepo
from billing.src.repositories.billing_cycle import BillingCycleRepo
from billing.src.repositories.user import UserRepo
from billing.src.dto.billing import TotalIncomeResponse, UserReportResponse
from billing.src.db.tables import User


class BillingService:
    def __init__(self, user_repo: UserRepo, transactions_repo: BillingTransactionRepo, cycle_repo: BillingCycleRepo):
        self.user_repo = user_repo
        self.transactions_repo = transactions_repo
        self.cycle_repo = cycle_repo

    async def get_total_income(self, day: datetime.date | None) -> TotalIncomeResponse:
        day = day or datetime.date.today()
        billing_cycle = await self.cycle_repo.get_cycle(date=day, is_active=day == datetime.date.today())
        return TotalIncomeResponse(date=day, total_income=billing_cycle.total_income if billing_cycle else 0)

    async def get_user_report(self, user: User) -> UserReportResponse:
        day = datetime.date.today()
        transactions = await self.transactions_repo.get_transactions(user_id=user.public_id, date=day)
        return UserReportResponse(user_id=user.public_id, user_balance=user.balance, user_auditlog=transactions)

