from sqlalchemy.orm import Session

from app.modules.account import account_repository
from app.modules.account.user_model import User


def update_account(
    db: Session,
    user: User,
    data,
):
    updates = data.model_dump(
        exclude_unset=True,
    )

    return account_repository.update_user(
        db=db,
        user=user,
        updates=updates,
    )


def delete_account(
    db: Session,
    user: User,
):
    account_repository.delete_user(
        db=db,
        user=user,
    )