from collections.abc import Generator

from app.database.database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
        print("Neon Db Connected Succesfully")
    finally:
        db.close()