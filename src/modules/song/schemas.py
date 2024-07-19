from pydantic import BaseModel

from src.modules.utils import StringifyableUrl


class CreateSong(BaseModel):
    name: str
    file: StringifyableUrl
    cover: StringifyableUrl | None = None


class ViewSong(BaseModel):
    id: int
    name: str
    file: StringifyableUrl
    cover: StringifyableUrl | None = None


class UpdateSong(BaseModel):
    id: int
    name: str | None = None
    file: StringifyableUrl | None = None
    cover: StringifyableUrl | None = None
