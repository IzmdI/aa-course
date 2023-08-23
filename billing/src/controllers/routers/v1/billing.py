import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from billing.src.db.tables import User
from billing.src.controllers.stub import Stub
from billing.src.controllers.dependencies import get_current_accountant_user, get_current_active_user
from billing.src.services.billing import BillingService
from billing.src.dto.billing import TotalIncomeResponse, UserReportResponse

router = APIRouter(tags=["billing"], prefix="/billing")


@router.get("/total-income", response_model=TotalIncomeResponse)
async def get_total_income(
    day: Annotated[
        datetime.date | None, Query(example="2023-08-25", description="отчётный день в формате ГГГГ-ММ-ДД")
    ] = None,
    user: User = Depends(get_current_accountant_user),  # noqa
    service: BillingService = Depends(Stub(BillingService)),
) -> TotalIncomeResponse:
    return await service.get_total_income(day)


@router.get("/report", response_model=UserReportResponse)
async def get_total_income(
    user: User = Depends(get_current_active_user),
    service: BillingService = Depends(Stub(BillingService)),
) -> UserReportResponse:
    return await service.get_user_report(user)
