from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import LoggingDestinationEnum


class Settings(BaseSettings):
    app_name: str = "Fast API"
    logging_level: str = "INFO"
    logging_destination: str = LoggingDestinationEnum.STDOUT_HUMAN_READABLE
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    algorithm: str = "HS256"
    jwt_secret_key: str
    db_user: str
    db_password: str
    db_name: str
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()


ORIGINS = [
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8000",
]
