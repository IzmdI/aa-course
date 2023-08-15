from db.tables.user import UserRole
from dto.base import BaseSchema, ORMBaseSchema


class UserDTO(ORMBaseSchema):
    username: str
    email: str | None
    role: UserRole | None
    bill: int | None


class UserCreateDTO(BaseSchema):
    username: str
    password: str
    email: str
    role: UserRole | None = UserRole.WORKER
    bill: int


class UserUpdateDTO(BaseSchema):
    username: str | None
    password: str | None
    email: str | None
    role: UserRole | None
    bill: int | None
    is_active: bool | None


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    sub: str | None
