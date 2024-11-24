import logging
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlmodel import Session, select

from app.core.config import settings
from app.core.logger import get_advanced_logger

log = get_advanced_logger("DatabaseLogger", level=logging.DEBUG)


engine = create_engine(str(settings.sqlalchemy_db_uri))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def check_db(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        log.error(e)
        raise e
