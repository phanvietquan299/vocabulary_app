from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "vocab_app"
    postgres_host: str = "db"
    postgres_port: int = 5433
    database_url: str = "postgresql://postgres:postgres@db:5433/vocab_app"
    secret_key: str = "your_super_secret_key_for_jwt"
    access_token_expire_minutes: int = 30
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
