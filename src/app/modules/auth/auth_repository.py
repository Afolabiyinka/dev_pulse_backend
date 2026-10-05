from sqlalchemy.orm import Session

from app.modules.account.account_repository import normalize_email
from app.modules.account.user_model import User


def create_user(
    db: Session,
    email: str,
    password: str | None = None,
    github_id: int | None = None,
    github_username: str | None = None,
    github_name: str | None = None,
    avatar: str | None = None,
    github_authenticated: bool = False,
):
    user = User(
        email=normalize_email(email),
        password=password,
        github_id=github_id,
        github_username=github_username,
        github_name=github_name,
        avatar=avatar,
        github_authenticated=github_authenticated,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
