from pydantic import BaseModel


class CreateAlbum(BaseModel):
    name: str
    cover: bytes | None = None


class ViewAlbum(BaseModel):
    id: int
    name: str
    cover: bytes | None = None


class UpdateAlbum(BaseModel):
    id: int
    name: str | None = None
    cover: bytes | None = None
