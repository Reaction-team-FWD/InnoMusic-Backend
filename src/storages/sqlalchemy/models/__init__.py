from .base import Base

# Add all models here
from .user import User
from .album import Album
from .song import Song
from .author_album import AuthorAlbum
from .author_song import AuthorSong

__all__ = [
    "Base",
    "User",
    "Album",
    "Song",
    "AuthorAlbum",
    "AuthorSong",
]
