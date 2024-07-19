from pydantic import BaseModel


class CreateSong(BaseModel):
    name: str
    file: bytes
    cover: bytes | None = None


class ViewSong(BaseModel):
    id: int
    name: str
    file: bytes
    cover: bytes | None = None


class UpdateSong(BaseModel):
    id: int
    name: str | None = None
    file: bytes | None = None
    cover: bytes | None = None
