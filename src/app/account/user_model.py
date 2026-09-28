from sqlalchemy import String, Boolean, BigInteger
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

    password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    avatar: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    github_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=True,
    )

    github_username: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    github_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    github_authenticated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )