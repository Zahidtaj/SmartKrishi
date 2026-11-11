"""SQLAlchemy database engine, session factory, and initialization helpers."""

from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for SmartKrishi relational models (SQLite & PostgreSQL compatible)."""


def _create_engine_from_url(database_url: str):
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
        if ":///" in database_url and not database_url.endswith(":memory:"):
            db_file = Path(database_url.split("///", 1)[1])
            db_file.parent.mkdir(parents=True, exist_ok=True)

    eng = create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        future=True,
    )

    if database_url.startswith("sqlite"):
        @event.listens_for(eng, "connect")
        def _set_sqlite_pragma(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    return eng


settings = get_settings()
engine = _create_engine_from_url(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a scoped SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(target_engine=None) -> None:
    """Create database tables if they do not exist."""
    import backend.models  # noqa: F401
    Base.metadata.create_all(bind=target_engine or engine)
