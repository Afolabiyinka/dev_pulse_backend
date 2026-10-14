from sqlalchemy.orm import Session
from app.core.encryption_helpers import decrypt_token
from app.modules.account import account_repository
from app.modules.account import account_repository
from app.modules.auth.auth_validation import LoginRequest, SignUpRequest
from app.modules.github import github_services
from app.core.security import hash_password, verify_password


def register_user(
    db: Session,
    data: SignUpRequest,
):
    existing_user = account_repository.get_user_by_email(email=data.email, db=db)
    if existing_user:
        raise ValueError("Email already in use")

    hashed = hash_password(data.password)
    return account_repository.create_user(db, data.email, hashed)


def authenticate_user(db: Session, data: LoginRequest):
    user = account_repository.get_user_by_email(db=db, email=data.email)

    if not user or user.password is None or not verify_password(data.password, user.password):
        return None
    return user


async def authenticate_github_user(db: Session, github_token: str):

    decrypted_token = decrypt_token(github_token)
    github_user = await github_services.get_github_user(decrypted_token)
    github_email = await github_services.get_github_email(decrypted_token)

    if not github_email:
        raise ValueError("No verified GitHub email found")

    user = account_repository.get_user_by_email(
        db=db,
        email=github_email,
    )

    if user:
        user.github_id = github_user["id"]
        user.github_username = github_user["login"]
        user.github_name = github_user.get("name")
        user.avatar = github_user.get("avatar_url")
        user.github_authenticated = True
        user.github_token = github_token

        db.commit()
        db.refresh(user)
        return user

    user = account_repository.create_user(
        db=db,
        email=github_email,
        password=None,
        github_id=github_user["id"],
        github_username=github_user["login"],
        github_name=github_user.get("name"),
        avatar=github_user.get("avatar_url"),
        github_authenticated=True,
        github_token=github_token
    )

    return user


