"""Config module."""

from pydantic_settings import BaseSettings

from src.utils.env import env


class Settings(BaseSettings):
    """Application settings."""

    # Project
    PROJECT_NAME: str = env.project_name
    VERSION: str = env.version

    # Database
    DATABASE_URL: str = env.database_url

settings = Settings()
