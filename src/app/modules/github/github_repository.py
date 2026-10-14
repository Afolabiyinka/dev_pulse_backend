import httpx

from fastapi import HTTPException

GITHUB_API_URL = "https://api.github.com"


async def fetch_github_repositories(
    github_token: str,
    page: int,
    per_page: int,
):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    params = {
        "page": page,
        "per_page": per_page,
        "sort": "updated",
        "direction": "desc",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{GITHUB_API_URL}/user/repos",
            headers=headers,
            params=params,
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Failed to retrieve GitHub repositories.",
        )

    return response.json()
