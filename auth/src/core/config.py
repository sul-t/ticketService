from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Setting(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / '.env')


config = Setting()


def get_db_uri() -> str:
    return f'mongodb://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}'

def get_auth_data() -> dict[str, str]:
    return {'secret_key': config.SECRET_KEY, 'algorithm': config.ALGORITHM}
