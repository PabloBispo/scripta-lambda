from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    GROQ_API_KEY: str

    POSTGRES_USER: str | None = "postgres"
    POSTGRES_PASSWORD: str | None = "postgres"
    POSTGRES_SERVER: str | None = "localhost"
    POSTGRES_PORT: int | None = 5432
    POSTGRES_DB: str = "postgres"

    POSTGRES_DB_URI: str | None = None

    @computed_field
    @property
    def sqlalchemy_db_uri(self) -> PostgresDsn:
        if self.POSTGRES_DB_URI:
            return self.POSTGRES_DB_URI

        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
