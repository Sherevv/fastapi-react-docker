from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    broker_url: str = Field(..., env='BROKER_URL')
    result_backend: str = Field(..., env='CELERY_RESULT_BACKEND')


settings = Settings()
