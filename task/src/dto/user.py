from uuid import UUID

from db.tables import UserRole
from dto.base import BaseSchema


class TokenPayload(BaseSchema):
    sub: str | None


class UserDTO(BaseSchema):
    public_id: UUID
    username: str
    role: UserRole
    email: str


class UserCreateDTO(BaseSchema):
    public_id: UUID
    username: str
    role: UserRole
    email: str


class UserUpdateDTO(BaseSchema):
    public_id: UUID
    username: str
    role: UserRole
    email: str
