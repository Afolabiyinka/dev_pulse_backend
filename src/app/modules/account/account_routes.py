from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.account import account_service
from app.modules.account.account_repository import get_user_by_id
from app.modules.account.account_schema import UpdateAccountRequest, UserResponse
from app.modules.auth.auth_dependency import auth_middleware
from app.database.db_session import get_db
from app.core.rate_limiter import limiter, GLOBAL_RATE_LIMIT

AccountRouter = APIRouter(
    prefix="/account",
    tags=["Account"],
    # dependencies=[Depends(auth_middleware)],
)


@AccountRouter.get("/me", name="Get Account Information", response_model=UserResponse)
@limiter.limit(GLOBAL_RATE_LIMIT)
def get_user(
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@AccountRouter.patch("/me", name="Edit account information", response_model=UserResponse)
@limiter.limit(GLOBAL_RATE_LIMIT)
def edit_account(
    data: UpdateAccountRequest,
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return account_service.update_account(db=db, user=user, data=data)

@AccountRouter.delete("/me", name="Delete your account",  status_code=status.HTTP_204_NO_CONTENT,
)

def delete_account(
    user_id: UUID = Depends(auth_middleware),
    db: Session = Depends(get_db),
) -> None:
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    account_service.delete_account(db=db, user=user)

