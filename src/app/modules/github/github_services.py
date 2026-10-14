
from uuid import UUID
import httpx

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core import encryption_helpers
from app.modules.github import github_repository
from app.modules.account import account_repository
from app.core.config import envVariables


async def get_github_repositories(
    user_id: UUID,
    page: int,
    per_page: int,
    db: Session,
):
    user = account_repository.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if not user.github_token:
        raise HTTPException(
            status_code=400,
            detail="GitHub account is not connected",
        )

    decrypted_token = encryption_helpers.decrypt_token(user.github_token)

    repositories = await github_repository.fetch_github_repositories(
        github_token=decrypted_token,
        page=page,
        per_page=per_page,
        
    )

    return {
        "repositories": repositories,
        "page": page,
        "per_page": per_page,
        "has_more": len(repositories) == per_page,
    }


# Exchange Github code for an access token
async def exchange_github_code(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": envVariables.github_client_id,
                "client_secret": envVariables.github_client_secret,
                "code": code,
                "redirect_uri": envVariables.github_redirect_uri,
            },
            headers={
                "Accept": "application/json",
            },
        )

    response.raise_for_status()
    data = response.json()
    return data["access_token"]


#Getting user info

import httpx
async def get_github_user(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )

    response.raise_for_status()
    return response.json()


async def get_github_email(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
            },
        )

    response.raise_for_status()

    emails = response.json()

    primary_email = next(
        (
            email["email"]
            for email in emails
            if email["primary"] and email["verified"]
        ),
        None,
    )

    return primary_email