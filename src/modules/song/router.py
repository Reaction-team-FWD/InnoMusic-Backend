from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ObjectNotFound
from src.api.shared import Shared
from src.modules.auth.dependencies import VerifiedDep
from src.modules.song.api_schemas import SongViewApi, CreateSongApi, UpdateSongApi
from src.modules.song.repository import SongRepository
from src.modules.song.schemas import ViewSong, CreateSong, UpdateSong
from src.modules.user.repository import UserRepository

router = APIRouter(prefix="/song", tags=["Songs"])


@router.get("/all")
async def get_all_songs() -> list[SongViewApi]:
    song_repository = Shared.f(SongRepository)
    user_repository = Shared.f(UserRepository)
    async with Shared.f(AsyncSession) as session:
        songs = await song_repository.get_all(session)
        response: list[SongViewApi] = []
        for song in songs:
            authors_ids = await song_repository.get_author_ids(session, song.id)
            authors = []
            for id_ in authors_ids:
                authors.append((await user_repository.read(id_, session)).name)
            response.append(SongViewApi(**song.model_dump(), authors=authors))
    return response


@router.get("/{song_id}")
async def get_song(song_id: int) -> SongViewApi:
    """
    Get song info
    """
    song_repository = Shared.f(SongRepository)
    user_repository = Shared.f(UserRepository)
    async with Shared.f(AsyncSession) as session:
        song = await song_repository.read(session, song_id)
        if song is None:
            raise ObjectNotFound()
        authors_ids = await song_repository.get_author_ids(session, song_id)
        authors = []
        for id_ in authors_ids:
            authors.append((await user_repository.read(id_, session)).name)
    return SongViewApi(**song.model_dump(), authors=authors)


@router.post("/create", status_code=201)
async def create_song(song: CreateSongApi, user: VerifiedDep) -> SongViewApi:
    """
    Create song
    """
    song_repository = Shared.f(SongRepository)
    async with Shared.f(AsyncSession) as session:
        view_song: ViewSong = await song_repository.create(
            session, CreateSong.model_validate(song, from_attributes=True)
        )
        await song_repository.add_authors(session, view_song.id, [user.id] + (song.extra_authors or []))

    return SongViewApi(**view_song.model_dump(), authors=[user.id])


@router.put("/{song_id}")
async def update_song(song_id: int, song: UpdateSongApi, _user: VerifiedDep) -> None:
    song_repository = Shared.f(SongRepository)
    async with Shared.f(AsyncSession) as session:
        if not await song_repository.exists(session, song_id):
            raise ObjectNotFound()
        await song_repository.update(session, UpdateSong(**song.model_dump(), id=song_id))


@router.delete("/{song_id}")
async def delete_song(song_id: int, _user: VerifiedDep) -> None:
    song_repository = Shared.f(SongRepository)
    async with Shared.f(AsyncSession) as session:
        if not await song_repository.exists(session, song_id):
            raise ObjectNotFound()
        await song_repository.delete(session, song_id)
