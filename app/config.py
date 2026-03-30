import os

from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENV", "local")


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: str = env
    debug: bool = True
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=f".env.{env}",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
