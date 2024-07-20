from pydantic import BaseModel

from src.modules.utils import StringifyableUrl


class CreateSongApi(BaseModel):
    name: str
    file: StringifyableUrl = "https://www.ostmusic.org/sound/track/undertale/100.%20MEGALOVANIA.mp3"
    cover: StringifyableUrl | None = (
        "https://inno-music-frontend.vercel.app/_next/image?url=%2Fimg%2FalbumCover.png&w=750&q=75"
    )
    extra_authors: list[int] | None = None


class SongViewApi(BaseModel):
    id: int
    name: str
    file: StringifyableUrl
    cover: StringifyableUrl | None = None
    authors: list[str]


class UpdateSongApi(BaseModel):
    name: str | None = None
    file: StringifyableUrl | None = None
    cover: StringifyableUrl | None = None
