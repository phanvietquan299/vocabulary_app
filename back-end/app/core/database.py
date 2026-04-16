import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def check_database_connection(max_retries: int = 10, delay_seconds: int = 3) -> None:
    last_error = None

    for _ in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except OperationalError as exc:
            last_error = exc
            time.sleep(delay_seconds)

    raise last_error


def ensure_vocabulary_media_columns() -> None:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE IF EXISTS vocabularies ADD COLUMN IF NOT EXISTS local_url VARCHAR(255)"))
