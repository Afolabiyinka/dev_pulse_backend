from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.modules.account.user_model import User

def normalize_email(email: str) -> str:
    return email.strip().casefold()






def create_user(
    db: Session,
    email: str,
    password: str | None = None,
    github_id: int | None = None,
    github_username: str | None = None,
    github_name: str | None = None,
    avatar: str | None = None,
    github_authenticated: bool = False,
    github_token: str | None = None,
):
    user = User(
        email=normalize_email(email),
        password=password,
        github_id=github_id,
        github_username=github_username,
        github_name=github_name,
        avatar=avatar,
        github_authenticated=github_authenticated,
        github_token=github_token
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def get_user_by_email(email, db: Session):
    normalized_email = normalize_email(email)
    return db.scalar(
        select(User).where(func.lower(User.email) == normalized_email)
    )

def get_user_by_id(db: Session, user_id: UUID):
    return db.scalar(
        select(User).where(User.id == user_id)
    )

def update_user(
    db: Session,
    user: User,
    updates: dict,
):
    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()