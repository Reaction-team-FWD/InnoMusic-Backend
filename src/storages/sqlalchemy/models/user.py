import typing
from enum import StrEnum

from sqlalchemy import Enum

from src.storages.sqlalchemy.utils import *

if typing.TYPE_CHECKING:
    from .album import Album
    from .song import Song


class UserRole(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


class User(Base, IdMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.DEFAULT)

    albums: Mapped[list["Album"]] = relationship(back_populates="authors", secondary="author_album")
    songs: Mapped[list["Song"]] = relationship(back_populates="authors", secondary="author_album")


__all__ = ["User", "UserRole"]
