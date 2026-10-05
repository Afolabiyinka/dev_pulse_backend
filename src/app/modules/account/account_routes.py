from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.account import account_service
from app.modules.account.account_repository import get_user_by_id
from app.modules.account.account_schema import UpdateAccountRequest, UserResponse
from app.modules.auth.auth_dependency import auth_middleware
from app.database.db_session import get_db

AccountRouter = APIRouter(
    prefix="/api/account",
    tags=["Account"],
    dependencies=[Depends(auth_middleware)],
)


def get_user(
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def edit_account(
    data: UpdateAccountRequest,
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return account_service.update_account(db=db, user=user, data=data)


def delete_account(
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
) -> None:
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    account_service.delete_account(db=db, user=user)


AccountRouter.add_api_route(
    "/me",
    get_user,
    methods=["GET"],
    name="Get account information",
    response_model=UserResponse,
)
AccountRouter.add_api_route(
    "/me",
    edit_account,
    methods=["PATCH"],
    name="Update account information",
    response_model=UserResponse,
)
AccountRouter.add_api_route(
    "/me",
    delete_account,
    methods=["DELETE"],
    name="Delete account",
    status_code=status.HTTP_204_NO_CONTENT,
)
