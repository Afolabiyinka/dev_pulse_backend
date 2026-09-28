from sqlalchemy import text

from app.database.database import engine


def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Neon DB Connected Successfully")

    except Exception as e:
        print(f"Neon DB Connection Failed: {e}")