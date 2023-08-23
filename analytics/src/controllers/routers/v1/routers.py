from fastapi import APIRouter

from analytics.src.controllers.routers.v1.healthcheck import router as healthcheck_router
from analytics.src.controllers.routers.v1.analytics import router as analytics_router

router = APIRouter(prefix="/api/v1")

router.include_router(healthcheck_router)
router.include_router(analytics_router)
