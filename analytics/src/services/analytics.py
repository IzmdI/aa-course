import datetime

from analytics.src.repositories.billing_transaction import BillingTransactionRepo
from analytics.src.repositories.billing_cycle import BillingCycleRepo
from analytics.src.repositories.user import UserRepo
from analytics.src.repositories.task import TaskRepo
from analytics.src.dto.billing import TaskRatingResponse, TotalIncomeResponse


class AnalyticsService:
    def __init__(
        self,
        user_repo: UserRepo,
        task_repo: TaskRepo,
        transactions_repo: BillingTransactionRepo,
        cycle_repo: BillingCycleRepo,
    ):
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.transactions_repo = transactions_repo
        self.cycle_repo = cycle_repo

    async def get_total_income(self, day: datetime.date | None) -> TotalIncomeResponse:
        day = day or datetime.date.today()
        billing_cycle = await self.cycle_repo.get_cycle(date=day, is_active=day == datetime.date.today())
        return TotalIncomeResponse(date=day, total_income=billing_cycle.total_income if billing_cycle else 0)

    async def get_unproductive_users(self) -> int:
        users = await self.user_repo.get_users_with_negative_balance()
        return len(users)

    async def get_task_rating(self) -> TaskRatingResponse:
        today_top = await self.task_repo.get_top_task("today")
        week_top = await self.task_repo.get_top_task("week")
        month_top = await self.task_repo.get_top_task("month")
        return TaskRatingResponse(today_top=today_top, week_top=week_top, month_top=month_top)
