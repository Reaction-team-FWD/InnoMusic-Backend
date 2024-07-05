from typing import Optional

from pydantic import BaseModel, Field

from src.modules.user.schemas import ViewUser


class VerificationResult(BaseModel):
    success: bool
    user: Optional[ViewUser] = None


class RegisterData(BaseModel):
    name: str = Field(description="User name")
    login: str = Field(description="User login")
    password: str = Field(description="User password")


class UserCredentialsFromDB(BaseModel):
    user_id: int
    password_hash: str


__all__ = ["VerificationResult", "UserCredentialsFromDB", "RegisterData"]
