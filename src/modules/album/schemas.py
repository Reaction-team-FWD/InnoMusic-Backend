from pydantic import BaseModel

from src.modules.utils import StringifyableUrl


class CreateAlbum(BaseModel):
    name: str
    cover: StringifyableUrl | None = None


class ViewAlbum(BaseModel):
    id: int
    name: str
    cover: StringifyableUrl | None = None


class UpdateAlbum(BaseModel):
    id: int
    name: str | None = None
    cover: StringifyableUrl | None = None
