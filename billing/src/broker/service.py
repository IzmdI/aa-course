from sqlalchemy.ext.asyncio import AsyncSession

from schema_registry import validators
from billing.src.broker.schemas import (
    Action,
    EventDataUserStreaming,
    ProducerEvent, TaskDoneData,
    TaskStreamingData,
    UserStreamingData,
    UserRoleData,
)
from billing.src.dto.user import UserCreateDTO, UserUpdateDTO
from billing.src.repositories.user import UserRepo
from billing.src.repositories.billing_transaction import BillingTransactionRepo
from billing.src.repositories.billing_cycle import BillingCycleRepo
from billing.src.db.tables import BillingCycle
from billing.src.dto.billing import TransactionCreateDTO
from billing.src.broker.dependencies import broker_settings
from billing.src.broker.producer import produce_event


class BrokerUserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepo(session)
        self.user_streaming_validator = validators.UserStreamingSchemaValidator()

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
        self.user_repo.session.expunge_all()
        user = await self.user_repo.get_user_by_public_id(user_data.public_id)
        message = EventDataUserStreaming(
            event_name="User Balance Updated",
            event_producer="Billing Service",
            event_version=1,
            event_data=UserStreamingData.from_model(user, action=Action.UPDATE),
        )
        topic = broker_settings.TOPIC_USER_STREAM
        if self.user_streaming_validator.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=topic, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате

    async def delete(self, msg: UserStreamingData) -> None:
        user_public_id = msg.public_id
        await self.user_repo.delete_user_by_public_id(user_public_id)


class BrokerBillingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transaction_repo = BillingTransactionRepo(session)
        self.billing_cycle_repo = BillingCycleRepo(session)
        self.user_repo = UserRepo(session)

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

    async def get_current_billing_cycle(self) -> BillingCycle:
        cycle = await self.billing_cycle_repo.get_current_billing_cycle()
        if not cycle:
            cycle = await self.billing_cycle_repo.create_cycle()
            await self.commit()
        return cycle

    async def create(self, msg: TaskStreamingData) -> None:
        current_cycle = await self.get_current_billing_cycle()
        transaction = TransactionCreateDTO(
            billing_cycle_id=current_cycle.public_id,
            user_id=msg.assignee_id,
            description=f"Task Assigned!\nTitle: {msg.title}\nDescription: {msg.description}",
            credit=msg.price,
        )
        user = await self.user_repo.get_user_by_public_id(msg.assignee_id)
        await self.transaction_repo.create_transaction(transaction)
        await self.user_repo.update_user(
            public_id=user.public_id,
            balance=user.balance - transaction.credit,
        )
        await self.billing_cycle_repo.update_cycle(
            public_id=current_cycle.public_id,
            total_income=current_cycle.total_income + transaction.credit,
        )

    async def update(self, msg: TaskStreamingData | TaskDoneData) -> None:
        current_cycle = await self.get_current_billing_cycle()
        transaction = TransactionCreateDTO(
            billing_cycle_id=current_cycle.public_id,
            user_id=msg.assignee_id,
            description=f"Task Assigned!\nTitle: {msg.title}\nDescription: {msg.description}"
            if isinstance(msg, TaskStreamingData)
            else "Task Done!",
            credit=msg.price if isinstance(msg, TaskStreamingData) else 0,
            debit=msg.fee if isinstance(msg, TaskDoneData) else 0,
        )
        user = await self.user_repo.get_user_by_public_id(msg.assignee_id)
        await self.transaction_repo.create_transaction(transaction)
        await self.user_repo.update_user(
            public_id=user.public_id,
            balance=user.balance - transaction.credit + transaction.debit,
        )
        await self.billing_cycle_repo.update_cycle(
            public_id=current_cycle.public_id,
            total_income=current_cycle.total_income + transaction.credit - transaction.debit,
        )

    async def delete(self, msg: TaskStreamingData) -> None:
        # TODO: подумать тут над логикой, что нужно делать (спросить у бизнеса)
        raise NotImplementedError
