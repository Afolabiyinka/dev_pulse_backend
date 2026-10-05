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