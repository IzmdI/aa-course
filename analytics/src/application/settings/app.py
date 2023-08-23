from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    RELOAD: bool = True
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8040
    CORS_ORIGINS: str = "*"

    class Config:
        env_prefix = "ANALYTICS_"
