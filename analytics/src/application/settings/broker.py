from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER: str = "localhost:9092"
    TOPIC_USER_STREAM: str = "UserStream"
    TOPIC_USER_ROLE: str = "UserRole"
    TOPIC_TASK_STREAM: str = "TaskStream"
    TOPIC_TASK_DONE: str = "TaskDone"

    class Config:
        env_prefix = "KAFKA_"
