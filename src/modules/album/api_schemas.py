from pydantic import BaseModel, Field

from src.modules.utils import StringifyableUrl


class CreateAlbumApi(BaseModel):
    name: str
    cover: StringifyableUrl | None = None
    extra_authors: list[int] | None = None
    songs: list[int] = Field(min_length=1)


class AlbumViewApi(BaseModel):
    id: int
    name: str
    cover: StringifyableUrl | None = None
    authors: list[int]
    songs: list[int] = Field(min_length=1)


class UpdateAlbumApi(BaseModel):
    name: str | None = None
    file: StringifyableUrl | None = None
    cover: StringifyableUrl | None = None
