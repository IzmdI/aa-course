from db.tables import UserRole
from dto.base import BaseSchema


class TokenPayload(BaseSchema):
    sub: str | None


class UserCreateDTO(BaseSchema):
    sso_id: int
    username: str
    role: UserRole
