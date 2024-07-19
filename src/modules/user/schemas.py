from pydantic import BaseModel, ConfigDict, Field

from src.modules.utils import StringifyableUrl
from src.storages.sqlalchemy.models.user import UserRole


class ViewUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    profile_picture: StringifyableUrl | None = None
    login: str
    password_hash: str = Field(exclude=True)
    role: UserRole = UserRole.DEFAULT

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class CreateUser(BaseModel):
    name: str | None = None
    login: str
    password_hash: str


class AuthorizedUserInfo(BaseModel):
    id: int
    login: str
    name: str
    role: UserRole = UserRole.DEFAULT


__all__ = ["ViewUser", "CreateUser", "AuthorizedUserInfo"]
