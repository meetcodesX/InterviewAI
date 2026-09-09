"""SQLAlchemy database setup and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


class Base(DeclarativeBase):
    pass


connect_args = {}
engine_kwargs = {"pool_pre_ping": True}
if "sqlite" in settings.DATABASE_URL:
    connect_args["check_same_thread"] = False
else:
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_tables_initialized = False


def init_db():
    """Create all tables lazily on first database access."""
    global _tables_initialized
    if not _tables_initialized:
        try:
            import models.models  # Ensure models are registered with Base metadata
            Base.metadata.create_all(bind=engine)
            _tables_initialized = True
        except Exception as e:
            # Re-raise so calling endpoint knows the failure
            raise e


def get_db():
    """Dependency that yields a database session."""
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
