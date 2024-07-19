import typing

from src.storages.sqlalchemy.utils import *

if typing.TYPE_CHECKING:
    from .album import Album
    from .user import User


class Song(Base, IdMixin):
    __tablename__ = "songs"

    name: Mapped[str] = mapped_column(nullable=False)
    file: Mapped[bytes] = mapped_column(nullable=False)
    album_id: Mapped[int | None] = mapped_column(
        ForeignKey("albums.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True
    )

    album: Mapped["Album"] = relationship(back_populates="songs")
    authors: Mapped[list["User"]] = relationship(back_populates="songs", secondary="author_song")


__all__ = ["Song"]
