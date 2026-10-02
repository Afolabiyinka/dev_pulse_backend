from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    avatar: str | None = None
    github_username: str | None = None
    github_name: str | None = None
    github_authenticated: bool

    model_config = {
        "from_attributes": True,
    }


class UpdateAccountRequest(BaseModel):
    avatar: str | None = None
    github_name: str | None = None
    github_username: str | None = None