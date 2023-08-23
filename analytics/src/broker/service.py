from sqlalchemy.ext.asyncio import AsyncSession

from analytics.src.broker.schemas import Action, TaskDoneData, TaskStreamingData, UserStreamingData, UserRoleData
from analytics.src.dto.user import UserCreateDTO, UserUpdateDTO
from analytics.src.repositories.user import UserRepo
from analytics.src.repositories.billing_transaction import BillingTransactionRepo
from analytics.src.repositories.billing_cycle import BillingCycleRepo
from analytics.src.dto.billing import BillingCycleCreateDTO, BillingCycleUpdateDTO, TransactionCreateDTO
from analytics.src.repositories.task import TaskRepo
from analytics.src.dto.task import TaskCreateDTO, TaskUpdateDTO


class BrokerUserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepo(session)

    async def __call__(self, msg: UserStreamingData | UserRoleData) -> None:
        match msg.action:
            case Action.CREATE:
                await self.create(msg)
            case Action.UPDATE:
                await self.update(msg)
            case Action.DELETE:
                await self.delete(msg)
            case _:
                pass
        await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def create(self, msg: UserStreamingData) -> None:
        user_data = UserCreateDTO(**msg.model_dump())
        await self.user_repo.create_user(user_data)

    async def update(self, msg: UserStreamingData | UserRoleData) -> None:
        user_data = UserUpdateDTO(**msg.model_dump())
        await self.user_repo.update_user(**user_data.model_dump(exclude_none=True))

    async def delete(self, msg: UserStreamingData) -> None:
        user_public_id = msg.public_id
        await self.user_repo.delete_user_by_public_id(user_public_id)


class BrokerTaskService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.task_repo = TaskRepo(session)

    async def __call__(self, msg: TaskStreamingData | TaskDoneData) -> None:
        match msg.action:
            case Action.CREATE:
                await self.create(msg)
            case Action.UPDATE:
                await self.update(msg)
            case Action.DELETE:
                await self.delete(msg)
            case _:
                pass
        await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def create(self, msg: TaskStreamingData) -> None:
        task_data = TaskCreateDTO(**msg.model_dump())
        await self.task_repo.create_task(task_data)

    async def update(self, msg: TaskStreamingData | TaskDoneData) -> None:
        task_data = TaskUpdateDTO(**msg.model_dump())
        await self.task_repo.update_task(**task_data.model_dump(exclude_none=True))

    async def delete(self, msg: TaskStreamingData) -> None:
        task_public_id = msg.public_id
        await self.task_repo.delete_task_by_public_id(task_public_id)


class BrokerBillingCycleService:
    # TODO: доделать стриммнг циклов: добавить схемы в аналитике и биллинге,
    #  добавить схемы в схема_реджистри, добавить продюсинг событий в биллинге
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.cycle_repo = BillingCycleRepo(session)

    async def __call__(self, msg: BillingCycleStreamingData) -> None:
        match msg.action:
            case Action.CREATE:
                await self.create(msg)
            case Action.UPDATE:
                await self.update(msg)
            case Action.DELETE:
                await self.delete(msg)
            case _:
                pass
        await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def create(self, msg: BillingCycleStreamingData) -> None:
        cycle_data = BillingCycleCreateDTO(**msg.model_dump())
        await self.cycle_repo.create_cycle(**cycle_data.model_dump(exclude_none=True))

    async def update(self, msg: BillingCycleStreamingData) -> None:
        cycle_data = BillingCycleUpdateDTO(**msg.model_dump())
        await self.cycle_repo.update_cycle(**cycle_data.model_dump(exclude_none=True))

    async def delete(self, msg: BillingCycleStreamingData) -> None:
        cycle_public_id = msg.public_id
        await self.cycle_repo.delete_cycle_by_public_id(cycle_public_id)


class BrokerBillingTransactionService:
    # TODO: доделать стриммнг транзакций: добавить схемы в аналитике и биллинге,
    #  добавить схемы в схема_реджистри, добавить продюсинг событий в биллинге
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transaction_repo = BillingTransactionRepo(session)

    async def __call__(self, msg: BillingTransactionStreamingData) -> None:
        match msg.action:
            case Action.CREATE:
                await self.create(msg)
            case Action.UPDATE:
                await self.update(msg)
            case Action.DELETE:
                await self.delete(msg)
            case _:
                pass
        await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def create(self, msg: BillingTransactionStreamingData) -> None:
        transaction_data = TransactionCreateDTO(**msg.model_dump())
        await self.transaction_repo.create_transaction(**transaction_data.model_dump(exclude_none=True))

    async def update(self, msg: BillingTransactionStreamingData) -> None:
        # UPDATE транзакций невозможен
        raise NotImplementedError

    async def delete(self, msg: BillingTransactionStreamingData) -> None:
        # DELETE транзакций невозможен
        raise NotImplementedError
