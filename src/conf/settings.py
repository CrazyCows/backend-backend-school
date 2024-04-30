from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class PostgresSettings(BaseSettings):
    host: str = Field(
        default="backend_postgres",
        description="Postgres host",
    )
    port: int = Field(
        default=5432,
        description="Postgres port",
    )
    database: str = Field(
        default="backend_school",
        description="Postgres database",
    )
    user: str = Field(
        default="firstuser",
        description="Postgres user",
    )
    password: str = Field(
        default="Studyhard1234.",
        description="Postgres password",
    )

    model_config = SettingsConfigDict(env_prefix="postgres_backend_school_")


class Settings(BaseSettings):

    class Config:
        env_file = ".env"
        env_prefix = ""
        env_file_encoding = "utf-8"
        extra = "ignore"

    database_config: PostgresSettings = PostgresSettings()

    @property
    def postgres_async(self) -> str:
        """Constructs SQLAlchemy URL based on database configuration."""
        return f"postgresql+asyncpg://{self.database_config.user}:{self.database_config.password}@{self.database_config.host}/{self.database_config.database}"

    @property
    def postgres(self) -> str:
        """Constructs SQLAlchemy URL based on database configuration."""
        return f"postgresql://{self.database_config.user}:{self.database_config.password}@{self.database_config.host}/{self.database_config.database}"

settings = Settings()
