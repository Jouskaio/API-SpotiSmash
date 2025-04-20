from contextlib import contextmanager
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db_session


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = get_db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()