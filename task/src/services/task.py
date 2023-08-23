from random import randint

from fastapi import HTTPException
from starlette import status

from task.src.application.settings.broker import Settings as Broker_settings
from task.src.broker.producer import produce_event
from task.src.broker.schemas import (
    Action,
    EventDataTaskDone,
    EventDataTaskStreaming,
    ProducerEvent,
    TaskStreamingData,
    TaskDoneData,
)
from task.src.db.tables import TaskStatus, User
from task.src.dto.schemas.request import CommonBaseQueryParamSchema, TaskFilterSchema
from task.src.dto.task import TaskCreateDTO
from task.src.repositories.task import TaskRepo
from task.src.repositories.user import UserRepo
from schema_registry import validators


class TaskService:
    def __init__(self, task_repo: TaskRepo, user_repo: UserRepo):
        self.task_repo = task_repo
        self.user_repo = user_repo
        # TODO: использовать фабрику или ещё что-то получше
        self.streaming_validator = validators.TaskStreamingSchemaValidator()
        self.streaming_validator_v2 = validators.TaskStreamingSchemaValidator(version=2)
        self.done_validator = validators.TaskDoneSchemaValidator()

    async def get_tasks(self, filters: TaskFilterSchema, common_params: CommonBaseQueryParamSchema, assignee: User):
        if filters.task_id:
            result = await self.task_repo.get_task_by_id(filters.task_id)
        else:
            result = await self.task_repo.get_tasks(
                assignee_id=assignee.public_id, common_params=common_params, **filters.model_dump(exclude_none=True)
            )
        return result

    async def create_task(self, task_data: TaskCreateDTO, owner: User, broker_settings: Broker_settings) -> None:
        task_data.owner_id = owner.public_id
        if not task_data.assignee_id:
            random_user = await self.user_repo.get_random_user()
            task_data.assignee_id = random_user[0].public_id
        task_data.price = randint(10, 20)
        task_data.fee = randint(20, 40)
        task_data.status = TaskStatus.ASSIGNED
        title = task_data.title
        if title.startswith("["):
            try:
                title, jira_id = title[1:].split("]")
            except ValueError:
                title, jira_id = title, None
            task_data.title = title
            task_data.jira_id = jira_id
        task = await self.task_repo.create_task(task_data)
        await self.task_repo.session.commit()
        message = EventDataTaskStreaming(
            event_name="Task Created",
            event_producer="Task Service",
            event_version=2,
            event_data=TaskStreamingData.from_model(task, action=Action.CREATE),
        )
        if self.streaming_validator_v2.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=broker_settings.TOPIC_TASK_STREAM, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате

    async def done_task(self, task_id: int, user: User, broker_settings: Broker_settings) -> None:
        task = await self.task_repo.get_task_by_id(task_id, by_undone_status=True)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if not task.assignee_id == user.public_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not this user task")
        await self.task_repo.update_task(task_id, status=TaskStatus.DONE)
        await self.task_repo.session.commit()
        self.task_repo.session.expunge(task)
        task = await self.task_repo.get_task_by_id(task_id)
        message = EventDataTaskDone(
            event_name="Task Done",
            event_producer="Task Service",
            event_version=1,
            event_data=TaskDoneData.from_model(task, action=Action.UPDATE),
        )
        if self.done_validator.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=broker_settings.TOPIC_TASK_DONE, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате

    async def refresh_tasks(self, broker_settings: Broker_settings) -> None:
        random_users = await self.user_repo.get_random_users()
        random_tasks = await self.task_repo.get_undone_tasks()
        users_count = len(random_users)
        for task in random_tasks:
            task.assignee_id = random_users[randint(0, users_count - 1)].public_id
        await self.task_repo.session.commit()
        self.task_repo.session.expunge_all()
        random_tasks = await self.task_repo.get_undone_tasks()
        for task in random_tasks:
            message = EventDataTaskStreaming(
                event_name="Task Assigned",
                event_producer="Task Service",
                event_version=2,
                event_data=TaskStreamingData.from_model(task, action=Action.UPDATE),
            )
            if self.streaming_validator_v2.is_valid(message.model_dump(mode="json")):
                event = ProducerEvent(topic=broker_settings.TOPIC_TASK_STREAM, value=message.model_dump())
                await produce_event(event, broker_settings)
                # TODO: добавить флоу по невалидной дате

    async def delete_task(self, task_id: int, broker_settings: Broker_settings) -> None:
        task = await self.task_repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        await self.task_repo.delete_task(task_id)
        await self.task_repo.session.commit()
        message = EventDataTaskStreaming(
            event_name="Task Deleted",
            event_producer="Task Service",
            event_version=2,
            event_data=TaskStreamingData.from_model(task, action=Action.DELETE),
        )
        if self.streaming_validator_v2.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=broker_settings.TOPIC_TASK_STREAM, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате
