import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import envVariables


logging.getLogger("sqlalchemy").setLevel(logging.ERROR)

engine = create_engine(
    envVariables.database_url,
    echo=False,
    pool_pre_ping=True,

)

SessionLocal = sessionmaker(
   autoflush=False,
   autocommit=False,
   bind=engine,
)


class Base(DeclarativeBase):
    pass

