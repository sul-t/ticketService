import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    RABBITMQ_HOST: str

    print(dotenv.find_dotenv())
    print(dotenv.dotenv_values(dotenv_path=dotenv.find_dotenv()))

    model_config = SettingsConfigDict(env_file=dotenv.find_dotenv())


settings: Setting = Setting()


def get_db_uri() -> str:
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


