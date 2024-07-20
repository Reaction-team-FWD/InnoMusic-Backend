from Levenshtein import distance
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shared import Shared
from src.modules.search.schemas_api import SearchEverywhereResponse, TopSearchResult
from src.modules.song.repository import SongRepository
from src.modules.song.router import get_song
from src.modules.song.schemas import ViewSong
from src.modules.user.repository import UserRepository
from src.modules.user.schemas import ViewUser

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/everywhere")
async def search_everywhere(query: str) -> SearchEverywhereResponse:
    """
    Search everywhere
    """
    user_repository = Shared.f(UserRepository)
    song_repository = Shared.f(SongRepository)
    async with Shared.f(AsyncSession) as session:
        candidates: list[tuple[str, ViewSong | ViewUser]]
        candidates = [(u.name, u) for u in await user_repository.get_all(session)]
        songs = [(s.name, s) for s in await song_repository.get_all(session)]
        candidates.extend(songs)

        _, top = max(candidates, key=lambda p: -distance(query, p[0]))
        songs.sort(key=lambda p: distance(query, p[0]))
        return SearchEverywhereResponse(
            top=TopSearchResult(
                type="user" if isinstance(top, ViewUser) else "song",
                value=top if isinstance(top, ViewUser) else await get_song(top.id),
            ),
            songs=[await get_song(s.id) for _, s in songs],
        )
