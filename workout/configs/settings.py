from pydantic-settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_URL: str = Field(default='postgres://workout:workout@db:5432/workout')

settings = Settings()