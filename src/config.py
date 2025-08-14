from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PRODUCTION = False
ENV_FILE_NAME = ".env" if PRODUCTION else ".dev.env"

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR.joinpath(BASE_DIR, ENV_FILE_NAME)

class Config(BaseSettings):
    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    # JWT
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # payment webhooks
    WEBHOOK_SECRET_KEY: str

    #test data
    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str
    DEFAULT_ADMIN_FULL_NAME: str

    DEFAULT_USER_EMAIL: str
    DEFAULT_USER_PASSWORD: str
    DEFAULT_USER_FULL_NAME: str


    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding="utf-8")

    def get_async_postgres_url_connection(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
config = Config()