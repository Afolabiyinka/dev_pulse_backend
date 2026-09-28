from sqlalchemy import text
from app.database.database import engine
from loguru import logger


def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.success("Neon DB Connected Successfully")

    except Exception as e:
        logger.error(f"Neon DB Connection Failed: {e}")