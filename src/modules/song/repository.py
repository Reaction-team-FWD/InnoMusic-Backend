__all__ = ["SongRepository"]

from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.song.schemas import ViewSong, CreateSong, UpdateSong
from src.modules.utils import get_available_ids
from src.storages.sqlalchemy.models import AuthorSong
from src.storages.sqlalchemy.models.song import Song


class SongRepository:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list["ViewSong"]:
        songs = await session.scalars(select(Song))
        return [ViewSong.model_validate(song, from_attributes=True) for song in songs]

    # ------------------ CRUD ------------------ #

    @classmethod
    async def create(cls, session: AsyncSession, song: CreateSong) -> ViewSong:
        song_dict = song.model_dump()
        song_dict["id"] = await get_available_ids(session, Song)
        new_song = Song(**song_dict)
        session.add(new_song)
        await session.commit()
        return ViewSong.model_validate(new_song, from_attributes=True)

    @classmethod
    async def read(cls, session: AsyncSession, id_: int) -> ViewSong | None:
        song = await session.get(Song, id_)
        if song:
            return ViewSong.model_validate(song, from_attributes=True)

    @classmethod
    async def update(cls, session: AsyncSession, song: UpdateSong):
        song_dict = song.model_dump(exclude_defaults=True)
        id_ = song_dict.pop("id")
        await session.execute(update(Song).where(id_ == Song.id).values(song_dict))
        await session.commit()

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(Song).where(id_ == Song.id))
        await session.commit()

    @classmethod
    async def get_author_ids(cls, session: AsyncSession, song_id: int) -> list[int]:
        return list(await session.scalars(select(AuthorSong.author_id).where(song_id == AuthorSong.song_id)))

    @classmethod
    async def add_authors(cls, session: AsyncSession, song_id: int, author_ids: list[int]):
        await session.execute(
            insert(AuthorSong).values([{"author_id": author_id, "song_id": song_id} for author_id in author_ids])
        )
        await session.commit()

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #
    @classmethod
    async def exists(cls, session: AsyncSession, song_id: int):
        return await session.get(Song, song_id) is not None
