from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.album.schemas import ViewAlbum, CreateAlbum, UpdateAlbum
from src.modules.utils import get_available_ids
from src.storages.sqlalchemy.models import AuthorAlbum, Song
from src.storages.sqlalchemy.models.album import Album


class AlbumRepository:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[ViewAlbum]:
        albums = await session.scalars(select(Album))
        return [ViewAlbum.model_validate(album, from_attributes=True) for album in albums]

    # ------------------ CRUD ------------------ #

    @classmethod
    async def create(cls, session: AsyncSession, album: CreateAlbum) -> ViewAlbum:
        album_dict = album.model_dump()
        album_dict["id"] = await get_available_ids(session, Album)
        new_album = Album(**album_dict)
        session.add(new_album)
        await session.commit()
        return ViewAlbum.model_validate(new_album, from_attributes=True)

    @classmethod
    async def read(cls, session: AsyncSession, id_: int) -> ViewAlbum | None:
        album = await session.get(Album, id_)
        if album:
            return ViewAlbum.model_validate(album, from_attributes=True)

    @classmethod
    async def update(cls, session: AsyncSession, album: UpdateAlbum):
        album_dict = album.model_dump(exclude_defaults=True)
        id_ = album_dict.pop("id")
        await session.execute(update(Album).where(id_ == Album.id).values(album_dict))
        await session.commit()

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(Album).where(id_ == Album.id))
        await session.commit()

    @classmethod
    async def get_author_ids(cls, session: AsyncSession, album_id: int) -> list[int]:
        return list(await session.scalars(select(AuthorAlbum.author_id).where(album_id == AuthorAlbum.album_id)))

    @classmethod
    async def add_authors(cls, session: AsyncSession, album_id: int, author_ids: list[int]):
        await session.execute(
            insert(AuthorAlbum).values([{"author_id": author_id, "album_id": album_id} for author_id in author_ids])
        )
        await session.commit()

    @classmethod
    async def get_song_ids(cls, session: AsyncSession, album_id: int) -> list[int]:
        return list(await session.scalars(select(Song.id).where(album_id == Song.album_id)))

    @classmethod
    async def add_songs(cls, session: AsyncSession, album_id: int, song_ids: list[int]):
        await session.execute(update(Song).where(Song.id.in_(song_ids)).values(album_id=album_id))
        await session.commit()

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #
    @classmethod
    async def exists(cls, session: AsyncSession, album_id: int):
        return await session.get(Album, album_id) is not None


__all__ = ["AlbumRepository"]
