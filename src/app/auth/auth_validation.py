from pydantic import BaseModel, EmailStr, Field, field_validator

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
         max_length=100,
     )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr):
        return str(value).lower()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
         max_length=100,
     )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr):
        return str(value).lower()