from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()  # loads .env

class Settings(BaseSettings):
    # DB
    database_url: str
    test_database_url: str | None = None

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App
    environment: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()
