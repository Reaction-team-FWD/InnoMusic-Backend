from typing import Literal

from pydantic import BaseModel

from src.modules.album.api_schemas import AlbumViewApi
from src.modules.song.api_schemas import SongViewApi
from src.modules.user.schemas import ViewUser


class TopSearchResult(BaseModel):
    type: Literal["song", "album", "user"]
    value: SongViewApi | AlbumViewApi | ViewUser


class SearchEverywhereResponse(BaseModel):
    top: TopSearchResult
    songs: list[SongViewApi]
