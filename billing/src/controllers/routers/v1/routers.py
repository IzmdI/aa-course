from fastapi import APIRouter

from billing.src.controllers.routers.v1.healthcheck import router as healthcheck_router
from billing.src.controllers.routers.v1.billing import router as billing_router

router = APIRouter(prefix="/api/v1")

router.include_router(healthcheck_router)
router.include_router(billing_router)
