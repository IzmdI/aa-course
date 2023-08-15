from fastapi import APIRouter, Depends, Path

from application.settings.broker import Settings as Broker_settings
from controllers.dependencies import get_current_active_user, get_current_moderator_user
from controllers.stub import Stub
from db.tables import User
from dto.schemas.request import CommonBaseQueryParamSchema, TaskFilterSchema
from dto.task import TaskCreateDTO
from services.task import TaskService

router = APIRouter(tags=["tasks"], prefix="/tasks")


@router.post("/create")
async def create_task(
    task_data: TaskCreateDTO,
    user: User = Depends(get_current_active_user),
    service: TaskService = Depends(Stub(TaskService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.create_task(task_data, owner=user, broker_settings=broker_settings)
    return {"create": "ok"}


@router.get("")
async def get_tasks(
    common_params: CommonBaseQueryParamSchema = Depends(),
    filter_schema: TaskFilterSchema = Depends(),
    user: User = Depends(get_current_active_user),
    service: TaskService = Depends(Stub(TaskService)),
):
    return await service.get_tasks(assignee=user, filters=filter_schema, common_params=common_params)


@router.put("/{task_id}/done")
async def update_task(
    task_id: int = Path(),
    user: User = Depends(get_current_active_user),  # noqa
    service: TaskService = Depends(Stub(TaskService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.done_task(task_id, user, broker_settings=broker_settings)
    return {"done": "ok"}


@router.post("/refresh")
async def update_task(
    user: User = Depends(get_current_moderator_user),  # noqa
    service: TaskService = Depends(Stub(TaskService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.refresh_tasks(broker_settings=broker_settings)
    return {"refresh": "ok"}


@router.delete("/{task_id}")
async def delete_task(
    task_id: int = Path(),
    user: User = Depends(get_current_moderator_user),  # noqa
    service: TaskService = Depends(Stub(TaskService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.delete_task(task_id, broker_settings=broker_settings)
    return {"delete": "ok"}
