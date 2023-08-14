from random import randint

from db.tables import TaskStatus, User
from dto.schemas.request import TaskFilterSchema
from dto.task import TaskCreateDTO
from repositories.task import TaskRepo
from repositories.user import UserRepo


class TaskService:
    def __init__(self, task_repo: TaskRepo, user_repo: UserRepo):
        self.task_repo = task_repo
        self.user_repo = user_repo

    async def get_tasks(self, filters: TaskFilterSchema, assignee: User):
        if filters.task_id:
            result = await self.task_repo.get_task_by_id(filters.task_id)
        else:
            result = await self.task_repo.get_tasks(**filters.dict(exclude_none=True), assignee_id=assignee.sso_id)
        return result

    async def create_task(self, task_data: TaskCreateDTO, owner: User) -> None:
        task_data.owner_id = owner.sso_id
        if not task_data.assignee_id:
            random_user = await self.user_repo.get_random_user()
            task_data.assignee_id = random_user.sso_id
        task_data.price = randint(10, 20)
        task_data.fee = randint(20, 40)
        await self.task_repo.create_task(task_data)
        # TODO: отправить CUD ивент о создании таски
        await self.task_repo.session.commit()

    async def done_task(self, task_id: int) -> None:
        if not await self.task_repo.is_exists(id=task_id):
            raise
        await self.task_repo.update_task(task_id, status=TaskStatus.DONE)
        # TODO: отправить CUD ивент о завершении таски
        # TODO: отправить BE ивент о завершении таски
        await self.task_repo.session.commit()

    async def refresh_tasks(self) -> None:
        random_users = await self.user_repo.get_random_users()
        random_tasks = await self.task_repo.get_undone_tasks()
        users_count = len(random_users)
        for task in random_tasks:
            task.assignee_id = random_users[randint(0, users_count - 1)].sso_id
        # TODO: отправить CUD ивент о переназначении таски
        # TODO: отправить BE ивент о переназначении таски
        await self.task_repo.session.commit()

    async def delete_task(self, task_id: int) -> None:
        if not await self.task_repo.is_exists(id=task_id):
            raise
        await self.task_repo.delete_task(task_id)
        await self.task_repo.session.commit()
