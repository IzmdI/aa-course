from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "2d88f9e8985004c72ca39dea0f96e8814d7ebac05205f0abeae9c32f5d0e1c4a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
