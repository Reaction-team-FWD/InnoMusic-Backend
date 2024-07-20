from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.modules.user.schemas import AuthorizedUserInfo


class VerificationResult(BaseModel):
    success: bool
    user: Optional[AuthorizedUserInfo] = None


class RegisterData(BaseModel):
    name: str = Field(description="User name")
    login: EmailStr = Field(description="User email")
    password: str = Field(description="User password")


class UserCredentialsFromDB(BaseModel):
    user_id: int
    password_hash: str


__all__ = ["VerificationResult", "UserCredentialsFromDB", "RegisterData"]
