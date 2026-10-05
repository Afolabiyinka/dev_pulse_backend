from sqlalchemy.orm import Session

from app.modules.account.account_repository import (
    update_user,
    delete_user,
)
from app.modules.account.user_model import User


def update_account(
    db: Session,
    user: User,
    data,
):
    updates = data.model_dump(
        exclude_unset=True,
    )

    return update_user(
        db=db,
        user=user,
        updates=updates,
    )


def delete_account(
    db: Session,
    user: User,
):
    delete_user(
        db=db,
        user=user,
    )