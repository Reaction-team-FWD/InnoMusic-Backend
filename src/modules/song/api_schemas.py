from pydantic import BaseModel

from src.modules.utils import StringifyableUrl


class CreateSongApi(BaseModel):
    name: str
    file: StringifyableUrl
    cover: StringifyableUrl | None = None
    extra_authors: list[int] | None = None


class SongViewApi(BaseModel):
    id: int
    name: str
    file: StringifyableUrl
    cover: StringifyableUrl | None = None
    authors: list[int]


class UpdateSongApi(BaseModel):
    name: str | None = None
    file: StringifyableUrl | None = None
    cover: StringifyableUrl | None = None
