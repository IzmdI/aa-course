from typing import Optional
from uuid import UUID

from db.tables import UserRole
from dto.base import BaseSchema


class TokenPayload(BaseSchema):
    sub: Optional[str] = None


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
