from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controllers.routers.v1.healthcheck import router as healthcheck_router
from controllers.routers.v1.task import router as task_router

# from dto.user import UserDTO

router = APIRouter(prefix="/api/v1")


@router.post(
    "/login",
    tags=["login"],
    # response_model=UserDTO,
)
async def log_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO: редирект в SSO на логин
    return {"error": "not implemented"}


router.include_router(healthcheck_router)
router.include_router(task_router)
