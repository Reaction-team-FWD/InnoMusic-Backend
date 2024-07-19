from src.storages.sqlalchemy.utils import *


class AuthorAlbum(Base):
    __tablename__ = "author_album"

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True
    )


__all__ = ["AuthorAlbum"]
