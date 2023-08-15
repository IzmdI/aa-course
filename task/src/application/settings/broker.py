from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER: str = "localhost:9092"
    TOPIC_USER_STREAM: str = "UserStream"
    TOPIC_USER_ROLE_CHANGED: str = "UserRoleChange"

    class Config:
        env_prefix = "KAFKA_"
