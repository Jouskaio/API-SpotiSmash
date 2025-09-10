from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.sqlite"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()