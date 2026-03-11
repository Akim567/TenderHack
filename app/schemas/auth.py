from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Credentials payload for login endpoint."""

    username: str = Field(min_length=1, examples=["demo"])
    password: str = Field(min_length=1, examples=["demo-password"])


class TokenResponse(BaseModel):
    """JWT contract placeholder for future auth implementation."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Minimal public representation of authenticated user."""

    username: str
    is_active: bool = True
