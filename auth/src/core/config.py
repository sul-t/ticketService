from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")


settings: Setting = Setting()


def get_db_uri() -> str:
    return f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"


def get_auth_data() -> dict[str, str]:
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
