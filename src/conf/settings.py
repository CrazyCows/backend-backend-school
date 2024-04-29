from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class PostgresSettings(BaseSettings):
    host: str = Field(
        default="localhost",
        description="Postgres host",
    )
    port: int = Field(
        default=5432,
        description="Postgres port",
    )
    database: str = Field(
        default="postgres",
        description="Postgres database",
    )
    user: str = Field(
        default="postgres",
        description="Postgres user",
    )
    password: str = Field(
        default="",
        description="Postgres password",
    )

    model_config = SettingsConfigDict(env_prefix="postgres_backend_school_")


class Settings(BaseSettings):
    postgres_settings: PostgresSettings = PostgresSettings()
