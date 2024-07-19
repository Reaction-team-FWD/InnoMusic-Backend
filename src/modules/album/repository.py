__all__ = ["AlbumRepository"]

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.album.schemas import ViewAlbum, CreateAlbum, UpdateAlbum
from src.modules.utils import get_available_ids
from src.storages.sqlalchemy.models.album import Album


class AlbumRepository:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list["ViewAlbum"]:
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

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #
