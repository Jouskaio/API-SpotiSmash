import logging
from pathlib import Path
from sqlalchemy import create_engine
from app.infrastructure.logging.setup_logging import setup_logging
from app.infrastructure.database.orm import Base

DB_PATH = Path(__file__).resolve().parent.parent.parent / "infrastructure" / "database" / "database.sqlite"

def init_db():
    db_dir = DB_PATH.parent
    db_dir.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        logging.info("Database already exists. Nothing to do.")
    else:
        logging.info("Creating new database with base schema...")
        engine = create_engine(f"sqlite:///{str(DB_PATH)}")
        Base.metadata.create_all(engine)
        logging.info("Database created successfully at %s", DB_PATH)

if __name__ == "__main__":
    setup_logging()
    logging.info("Initializing Spotify client...")
    init_db()