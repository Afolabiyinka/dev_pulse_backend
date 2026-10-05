from sqlalchemy.orm import Session
import httpx
from app.account.account_repository import get_user_by_email
from app.auth.auth_repository import create_user
from app.auth.auth_validation import LoginRequest, SignUpRequest
from app.auth.github_auth_services import get_github_email, get_github_user
from app.config import settings
from app.core.security import hash_password, verify_password


def register_user(
    db: Session,
    data: SignUpRequest,
):
    existing_user = get_user_by_email(email=data.email, db=db)
    if existing_user:
        raise ValueError("Email already in use")

    hashed = hash_password(data.password)
    return create_user(db, data.email, hashed)


def authenticate_user(db: Session, data: LoginRequest):
    user = get_user_by_email(db=db, email=data.email)

    if not user or user.password is None or not verify_password(data.password, user.password):
        return None
    return user


async def authenticate_github_user(db: Session, github_token: str):
    github_user = await get_github_user(github_token)
    github_email = await get_github_email(github_token)

    if not github_email:
        raise ValueError("No verified GitHub email found")

    user = get_user_by_email(
        db=db,
        email=github_email,
    )

    if user:
        user.github_id = github_user["id"]
        user.github_username = github_user["login"]
        user.github_name = github_user.get("name")
        user.avatar = github_user.get("avatar_url")
        user.github_authenticated = True

        db.commit()
        db.refresh(user)
        return user

    user = create_user(
        db=db,
        email=github_email,
        password=None,
        github_id=github_user["id"],
        github_username=github_user["login"],
        github_name=github_user.get("name"),
        avatar=github_user.get("avatar_url"),
        github_authenticated=True,
    )

    return user


async def exchange_github_code(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_redirect_uri,
            },
            headers={
                "Accept": "application/json",
            },
        )

    response.raise_for_status()
    data = response.json()
    return data["access_token"]
