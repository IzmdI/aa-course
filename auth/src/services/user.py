from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from application.settings.auth import Settings as Auth_settings
from application.settings.broker import Settings as Broker_settings
from broker.producer import produce_event
from broker.schemas import (
    Action,
    EventDataUserRole,
    EventDataUserStreaming,
    ProducerEvent,
    UserRoleData,
    UserStreamingData,
)
from db.tables import User, UserRole
from dto.user import UserCreateDTO, UserUpdateDTO
from repositories.user import UserRepo
from schema_registry import validators


class UserService:
    def __init__(self, user_repo: UserRepo, pwd_context: CryptContext):
        self.user_repo = user_repo
        self.pwd_context = pwd_context
        # TODO: использовать фабрику или ещё что-то получше
        self.streaming_validator = validators.UserStreamingSchemaValidator()
        self.role_validator = validators.UserRoleSchemaValidator()

    def decode_token(self, token: str, auth_settings: Auth_settings = Auth_settings()) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username

    async def get_current_user(self, auth_settings: Auth_settings, token: str) -> User:
        username, _ = self.decode_token(token, auth_settings)
        user = await self.user_repo.get_user(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_current_active_user(self, auth_settings: Auth_settings, token: str) -> User:
        current_user = await self.get_current_user(auth_settings, token)
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repo.get_user(username)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_access_token(
        self, auth_settings: Auth_settings, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta if expires_delta else timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
        return encoded_jwt

    async def create_user(self, user_data: UserCreateDTO, broker_settings: Broker_settings) -> None:
        user_data.password = self.get_password_hash(user_data.password)
        user = await self.user_repo.create_user(user_data)
        await self.user_repo.session.commit()
        message = EventDataUserStreaming(
            event_name="User Created",
            event_producer="Auth Service",
            event_version=1,
            event_data=UserStreamingData.from_model(user, action=Action.CREATE),
        )
        if self.streaming_validator.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=broker_settings.TOPIC_USER_STREAM, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате

    async def update_user(
        self, token: str, user_id: int, user_data: UserUpdateDTO, broker_settings: Broker_settings
    ) -> None:
        username = self.decode_token(token)
        user = await self.user_repo.get_user_by_id(user_id)
        action_user = await self.user_repo.get_user(username)
        if not user or not action_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if action_user.role not in (UserRole.ADMIN, UserRole.MODERATOR):
            if username != user.username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="The user doesn't have enough privileges",
                )
            if user_data.role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="The user doesn't have enough privileges",
                )
        if user_data.password:
            user_data.password = self.get_password_hash(user_data.password)
        await self.user_repo.update_user(user_id, **user_data.model_dump(exclude_none=True))
        await self.user_repo.session.commit()
        self.user_repo.session.expunge(user)
        user = await self.user_repo.get_user_by_id(user_id)
        if user_data.role:
            message = EventDataUserRole(
                event_name="User Role Changed",
                event_producer="Auth Service",
                event_version=1,
                event_data=UserRoleData.from_model(user, action=Action.UPDATE),
            )
            topic = broker_settings.TOPIC_USER_ROLE
            is_valid = self.role_validator.is_valid(message.model_dump(mode="json"))
        else:
            message = EventDataUserStreaming(
                event_name="User Created",
                event_producer="Auth Service",
                event_version=1,
                event_data=UserStreamingData.from_model(user, action=Action.CREATE),
            )
            topic = broker_settings.TOPIC_USER_STREAM
            is_valid = self.streaming_validator.is_valid(message.model_dump(mode="json"))
        if is_valid:
            event = ProducerEvent(topic=topic, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате

    async def delete_user(self, token: str, user_id: int, broker_settings: Broker_settings) -> None:
        username = self.decode_token(token)
        user = await self.user_repo.get_user_by_id(user_id)
        action_user = await self.user_repo.get_user(username)
        if not user or not action_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if action_user.role not in (UserRole.ADMIN.value, UserRole.MODERATOR.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        await self.user_repo.delete_user(user_id)
        await self.user_repo.session.commit()
        message = EventDataUserStreaming(
            event_name="User Deleted",
            event_producer="Auth Service",
            event_version=1,
            event_data=UserStreamingData.from_model(user, action=Action.DELETE),
        )
        if self.streaming_validator.is_valid(message.model_dump(mode="json")):
            event = ProducerEvent(topic=broker_settings.TOPIC_USER_STREAM, value=message.model_dump())
            await produce_event(event, broker_settings)
            # TODO: добавить флоу по невалидной дате
