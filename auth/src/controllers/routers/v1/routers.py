from fastapi import APIRouter

from auth.src.controllers.routers.v1.auth import router as auth_router
from auth.src.controllers.routers.v1.healthcheck import router as healthcheck_router

router = APIRouter(prefix="/api/v1")

router.include_router(healthcheck_router)
router.include_router(auth_router)
