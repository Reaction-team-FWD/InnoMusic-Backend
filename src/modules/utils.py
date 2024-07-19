import random
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storages.sqlalchemy.models.__mixin__ import IdMixin


async def get_available_ids(
    session: AsyncSession, class_: Type[IdMixin], count: int = 1, min_: int = 100_000, max_: int = 999_999
) -> list[int] | int:
    q = select(class_.id)
    excluded_ids = set(await session.scalars(q))
    excluded_ids: set[int]
    available_ids = set()
    while len(available_ids) < count:
        chosen_id = random.randint(min_, max_)
        if chosen_id not in excluded_ids:
            available_ids.add(chosen_id)
    return list(available_ids) if count > 1 else available_ids.pop()
