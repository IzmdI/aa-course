from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER: str = "localhost:9092"
    TOPIC_USER_STREAM: str = "UserStream"
    TOPIC_USER_ROLE_CHANGED: str = "UserRoleChange"
    TOPIC_TASK_STREAM: str = "TaskStream"
    TOPIC_TASK_STATUS_CHANGED: str = "TaskStatusChange"

    class Config:
        env_prefix = "KAFKA_"
