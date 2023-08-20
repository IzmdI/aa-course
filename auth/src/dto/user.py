from typing import Optional
from uuid import UUID

from db.tables.user import UserRole
from dto.base import BaseSchema, ORMBaseSchema


class UserDTO(ORMBaseSchema):
    public_id: UUID
    username: str
    email: Optional[str] = None
    role: Optional[UserRole] = None
    bill: Optional[int] = None


class UserCreateDTO(BaseSchema):
    username: str
    password: str
    email: str
    role: Optional[UserRole] = UserRole.WORKER
    bill: int


class UserUpdateDTO(BaseSchema):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    bill: Optional[int] = None
    is_active: Optional[bool] = None


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    sub: Optional[str] = None
