from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path

# Путь к .env: поднимаемся из utils/ -> app/ -> backend/ -> корень проекта cinema
ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
    )
    DATABASE_URL: Optional[str | None] = None
    POSTGRES_USER: Optional[str | None] = None
    POSTGRES_PASSWORD: Optional[str | None] = None
    POSTGRES_DB: Optional[str | None] = None
    POSTGRES_HOST: Optional[str | None] = None
    POSTGRES_PORT: Optional[str | None] = None

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
print(settings.get_db_url)