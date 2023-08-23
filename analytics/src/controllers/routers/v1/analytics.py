import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from analytics.src.db.tables import User
from analytics.src.controllers.stub import Stub
from analytics.src.controllers.dependencies import get_current_admin_user
from analytics.src.services.analytics import AnalyticsService
from analytics.src.dto.billing import TaskRatingResponse, TotalIncomeResponse, UserReportResponse

router = APIRouter(tags=["analytics"], prefix="/analytics")


@router.get("/total-income", response_model=TotalIncomeResponse)
async def get_total_income(
    day: Annotated[
        datetime.date | None, Query(example="2023-08-25", description="отчётный день в формате ГГГГ-ММ-ДД")
    ] = None,
    user: User = Depends(get_current_admin_user),  # noqa
    service: AnalyticsService = Depends(Stub(AnalyticsService)),
) -> TotalIncomeResponse:
    return await service.get_total_income(day)


@router.get("/unproductive-users")
async def get_unproductive_users(
    user: User = Depends(get_current_admin_user),  # noqa
    service: AnalyticsService = Depends(Stub(AnalyticsService)),
) -> UserReportResponse:
    return await service.get_unproductive_users()


@router.get("/task-fee-rating", response_model=TaskRatingResponse)
async def get_unproductive_users(
    user: User = Depends(get_current_admin_user),  # noqa
    service: AnalyticsService = Depends(Stub(AnalyticsService)),
) -> TaskRatingResponse:
    return await service.get_task_rating()
