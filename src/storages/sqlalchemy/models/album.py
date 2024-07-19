import typing

from src.storages.sqlalchemy.utils import *

if typing.TYPE_CHECKING:
    from .song import Song
    from .user import User


class Album(Base, IdMixin):
    __tablename__ = "albums"

    name: Mapped[str] = mapped_column(nullable=False)

    songs: Mapped[list["Song"]] = relationship(back_populates="album")
    authors: Mapped[list["User"]] = relationship(back_populates="albums", secondary="author_album")


__all__ = ["Album"]
