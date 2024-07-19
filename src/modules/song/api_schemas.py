from pydantic import BaseModel


class CreateSongApi(BaseModel):
    name: str
    file: bytes
    cover: bytes | None = None
    extra_authors: list[int] | None = None


class SongViewApi(BaseModel):
    id: int
    name: str
    file: bytes
    cover: bytes | None = None
    authors: list[int]


class UpdateSongApi(BaseModel):
    name: str | None = None
    file: bytes | None = None
    cover: bytes | None = None
