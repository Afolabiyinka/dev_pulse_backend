from collections.abc import Generator
from app.database.database import SessionLocal
from loguru import logger


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
        logger.success("Database session completed successfully")
    finally:
        db.close()