from typing import Any, Sequence

from sqlalchemy import Row, RowMapping, delete, func, select, update
from sqlalchemy.exc import IntegrityError

from db.tables import User, UserRole
from dto.user import UserCreateDTO
from repositories.repo_base import BaseRepository


class UserRepo(BaseRepository):
    async def is_exists(self, **kwargs) -> bool:
        query = select(select(User.id).filter_by(**kwargs).exists())
        result = await self.session.execute(query)
        return result.scalar()

    async def get_user(self, username: str) -> User | None:
        query = select(User).filter_by(username=username)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def get_random_user(self) -> User | None:
        query = select(User).filter(User.role.not_in((UserRole.ADMIN, UserRole.MODERATOR))).order_by(func.random())
        user = await self.session.execute(query)
        return user.first()

    async def get_random_users(self) -> list[User] | Sequence[Row | RowMapping | Any]:
        query = select(User).filter(User.role.not_in((UserRole.ADMIN, UserRole.MODERATOR))).order_by(func.random())
        users = await self.session.execute(query)
        return users.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).filter_by(id=user_id)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def create_user(self, user_data: UserCreateDTO) -> User:
        user = User(**user_data.dict(exclude_none=True))
        unique_fields_exceptions = await self.validate_uniques(user)
        if unique_fields_exceptions:
            raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)
        self.session.add(user)
        await self.session.flush([user])
        return user

    async def update_user(self, sso_id: int, **kwargs) -> None:
        try:
            query = update(User).values(**kwargs).filter_by(sso_id=sso_id)
            await self.session.execute(query)
        except IntegrityError:
            unique_fields_exceptions = await self.validate_uniques_by_values(User, kwargs)
            if unique_fields_exceptions:
                raise IntegrityError(params=unique_fields_exceptions, statement=None, orig=None)

    async def delete_user(self, sso_id: int) -> None:
        query = delete(User).filter_by(sso_id=sso_id)
        await self.session.execute(query)
