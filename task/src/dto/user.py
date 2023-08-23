from typing import Optional
from uuid import UUID

from task.src.db.tables import UserRole
from task.src.dto.base import BaseSchema


class TokenPayload(BaseSchema):
    sub: Optional[str] = None


class UserCreateDTO(BaseSchema):
    public_id: UUID
    username: Optional[str] = None
    role: UserRole
    email: Optional[str] = None


class UserUpdateDTO(BaseSchema):
    public_id: UUID
    username: Optional[str] = None
    role: Optional[UserRole] = None
    email: Optional[str] = None
