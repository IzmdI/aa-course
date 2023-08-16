from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from broker.schemas import Action, UserMessage
from dto.user import UserCreateDTO, UserUpdateDTO
from repositories.user import UserRepo


class BrokerUserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepo(session)

    async def __call__(self, msg: UserMessage) -> None:
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

    async def create(self, msg: UserMessage) -> None:
        user_data = UserCreateDTO(**asdict(msg))
        await self.user_repo.create_user(user_data)

    async def update(self, msg: UserMessage) -> None:
        user_data = UserUpdateDTO(**asdict(msg))
        await self.user_repo.update_user(**user_data.dict())

    async def delete(self, msg: UserMessage) -> None:
        user_public_id = msg.public_id
        await self.user_repo.delete_user_by_public_id(user_public_id)
