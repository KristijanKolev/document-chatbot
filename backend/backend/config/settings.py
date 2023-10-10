from typing import Any

from pydantic_settings import BaseSettings
from pydantic import field_validator, PostgresDsn, ValidationInfo


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    CHROMA_HOST: str
    CHROMA_PORT: int
    CHROMA_COLLECTION: str

    GITHUB_CLIENT_ID: str
    GITHUB_SECRET: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_DELTA: int = 15  # in minutes

    SESSIONS_LIMIT_PERIOD_LENGTH: int = 24  # in hours
    SESSIONS_LIMIT_PER_PERIOD: int = 10  # Amount of new sessions allowed in last SESSIONS_LIMIT_PERIOD_LENGTH hours


settings = Settings()
