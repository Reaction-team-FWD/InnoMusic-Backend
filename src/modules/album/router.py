from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ObjectNotFound
from src.api.shared import Shared
from src.modules.auth.dependencies import VerifiedDep
from src.modules.album.api_schemas import AlbumViewApi, CreateAlbumApi, UpdateAlbumApi
from src.modules.album.repository import AlbumRepository
from src.modules.album.schemas import ViewAlbum, CreateAlbum, UpdateAlbum

router = APIRouter(prefix="/album", tags=["Albums"])


@router.get("/all")
async def get_all_albums() -> list[AlbumViewApi]:
    album_repository = Shared.f(AlbumRepository)
    async with Shared.f(AsyncSession) as session:
        albums = await album_repository.get_all(session)
        response: list[AlbumViewApi] = []
        for album in albums:
            authors = await album_repository.get_author_ids(session, album.id)
            songs = await album_repository.get_song_ids(session, album.id)
            response.append(AlbumViewApi(**album.model_dump(), authors=authors, songs=songs))
    return response


@router.get("/{album_id}")
async def get_album(album_id: int) -> AlbumViewApi:
    """
    Get album info
    """
    album_repository = Shared.f(AlbumRepository)
    async with Shared.f(AsyncSession) as session:
        album = await album_repository.read(session, album_id)
        if album is None:
            raise ObjectNotFound()
        authors = await album_repository.get_author_ids(session, album_id)
        songs = await album_repository.get_song_ids(session, album.id)
    return AlbumViewApi(**album.model_dump(), authors=authors, songs=songs)


@router.post("/create", status_code=201)
async def create_album(album: CreateAlbumApi, user: VerifiedDep) -> AlbumViewApi:
    """
    Create album
    """
    authors = [user.id] + (album.extra_authors or [])
    album_repository = Shared.f(AlbumRepository)
    async with Shared.f(AsyncSession) as session:
        view_album: ViewAlbum = await album_repository.create(
            session, CreateAlbum.model_validate(album, from_attributes=True)
        )
        await album_repository.add_authors(session, view_album.id, authors)
        await album_repository.add_songs(session, view_album.id, album.songs)

    return AlbumViewApi(**view_album.model_dump(), authors=authors, songs=album.songs)


@router.put("/{album_id}")
async def update_album(album_id: int, album: UpdateAlbumApi, _user: VerifiedDep) -> None:
    album_repository = Shared.f(AlbumRepository)
    async with Shared.f(AsyncSession) as session:
        if not await album_repository.exists(session, album_id):
            raise ObjectNotFound()
        await album_repository.update(session, UpdateAlbum(**album.model_dump(), id=album_id))


@router.delete("/{album_id}")
async def delete_album(album_id: int, _user: VerifiedDep) -> None:
    album_repository = Shared.f(AlbumRepository)
    async with Shared.f(AsyncSession) as session:
        if not await album_repository.exists(session, album_id):
            raise ObjectNotFound()
        await album_repository.delete(session, album_id)
