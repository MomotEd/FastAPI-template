from contextvars import ContextVar
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import Engine, create_engine
from sqlmodel import Session
from app.core.settings import get_settings

database_session_context: ContextVar[Optional[Session]] = ContextVar("database_session", default=None)

database_engine: Optional[Engine] = None
last_database_engine_refresh: Optional[datetime] = None


def _get_database_engine() -> Engine:
    global database_engine, last_database_engine_refresh
    if (
        database_engine is None
        or last_database_engine_refresh is None
        or last_database_engine_refresh + timedelta(hours=1) < datetime.now()
    ):
        settings = get_settings()
        if settings.database_url is None:
            raise ValueError("Chimera database connection string is not set correctly.")
        connection_args = {
            "connect_timeout": 30,
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 30,
            "keepalives_count": 2,
        }
        if database_engine is not None:
            database_engine.dispose()
        database_engine = create_engine(settings.database_url, connect_args=connection_args)
        last_database_engine_refresh = datetime.now()
    return database_engine


async def database_dependency():
    global database_session_context
    try:
        local_database_engine = _get_database_engine()
        database_session_context.set(
            Session(
                local_database_engine,
                autoflush=True,
                autocommit=False,
                expire_on_commit=False,
            )
        )
        yield database_session_context.get()
    finally:
        database_session = database_session_context.get()
        if database_session is not None:
            database_session.close()
            database_session_context.set(None)


def get_database_session() -> Session:
    global database_session_context
    database_session = database_session_context.get()
    if database_session is None:
        raise ValueError(
            "Database session is not set. You must only request a database session from a function "
            "called by a FastAPI route that has a database_dependency injected."
        )
    return database_session
