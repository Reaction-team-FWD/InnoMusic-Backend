from src.storages.sqlalchemy.utils import *


class AuthorSong(Base):
    __tablename__ = "author_song"

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    song_id: Mapped[int] = mapped_column(
        ForeignKey("songs.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True
    )

    def __init__(self, author_id: int, song_id: int):
        super().__init__(author_id=author_id, song_id=song_id)


__all__ = ["AuthorSong"]
