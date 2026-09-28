from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    googleAuthenticated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    avatar: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )