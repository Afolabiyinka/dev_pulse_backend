from typing import Optional
import uuid
from sqlalchemy import UUID

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
        )
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

    @validates("email")
    def validate_email(self, key, value):
        if value is None:
            return value
        return value.strip().casefold()