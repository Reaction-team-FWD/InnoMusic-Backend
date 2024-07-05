__all__ = ["Shared", "SessionDep", "EnsureAdminDep"]

from typing import TypeVar, ClassVar, Callable, Union, Hashable, Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ForbiddenException

if TYPE_CHECKING:
    from src.modules.user.schemas import ViewUser


T = TypeVar("T")

CallableOrValue = Union[Callable[[], T], T]


class Shared:
    """
    Key-value storage with generic type support for accessing shared dependencies
    """

    __slots__ = ()

    providers: ClassVar[dict[type, CallableOrValue]] = {}

    @classmethod
    def register_provider(cls, key: type[T] | Hashable, provider: CallableOrValue):
        cls.providers[key] = provider

    @classmethod
    def f(cls, key: type[T] | Hashable) -> T:
        """
        Get shared dependency by key (f - fetch)
        """
        if key not in cls.providers:
            if isinstance(key, type):
                # try by classname
                key = key.__name__

                if key not in cls.providers:
                    raise KeyError(f"Provider for {key} is not registered")

            elif isinstance(key, str):
                # try by classname
                for cls_key in cls.providers.keys():
                    if cls_key.__name__ == key:
                        key = cls_key
                        break
                else:
                    raise KeyError(f"Provider for {key} is not registered")

        provider = cls.providers[key]

        if callable(provider):
            return provider()
        else:
            return provider


async def get_session():
    async with Shared.f(AsyncSession) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


from src.modules.auth.dependencies import VerifiedDep  # noqa: E402


async def get_user(verification: VerifiedDep) -> "ViewUser":
    if not verification.success:
        raise ForbiddenException()
    return verification.user


UserDep = Annotated["ViewUser", Depends(get_user)]


async def ensure_admin(user: UserDep):
    if not user.is_admin:
        raise ForbiddenException()
    return user


EnsureAdminDep = Annotated["ViewUser", Depends(ensure_admin)]
