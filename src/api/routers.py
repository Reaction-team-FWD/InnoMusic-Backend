from src.config import settings
from src.config_schema import Environment
from src.modules.user.router import router as router_users
from src.modules.auth.router import router as router_auth
from src.modules.song.router import router as router_song
from src.modules.album.router import router as router_album
from src.modules.search.router import router as router_search

routers = [router_users, router_auth, router_song, router_album, router_search]

if settings.environment == Environment.DEVELOPMENT:
    from src.modules.dev.router import router as router_dev

    routers.append(router_dev)

__all__ = ["routers"]
