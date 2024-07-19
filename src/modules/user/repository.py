__all__ = ["UserRepository"]

from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.schemas import ViewUser, CreateUser
from src.modules.utils import get_available_ids
from src.storages.sqlalchemy.models.user import User


class UserRepository:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list["ViewUser"]:
        q = select(User)
        users = await session.scalars(q)
        if users:
            return [ViewUser.model_validate(user, from_attributes=True) for user in users]

    # ------------------ CRUD ------------------ #

    @classmethod
    async def create(cls, user: CreateUser, session: AsyncSession) -> ViewUser:
        user_dict = user.model_dump()
        user_dict["id"] = await get_available_ids(session, User)
        q = insert(User).values(user_dict).returning(User)
        new_user = await session.scalar(q)
        await session.commit()
        return ViewUser.model_validate(new_user)

    @classmethod
    async def create_superuser(cls, login: str, password_hash: str, session: AsyncSession) -> ViewUser:
        user_dict = {
            "id": await get_available_ids(session, User),
            "login": login,
            "name": "Superuser",
            "password_hash": password_hash,
            "role": "admin",
        }

        q = insert(User).values(user_dict).returning(User)
        new_user = await session.scalar(q)
        await session.commit()
        return ViewUser.model_validate(new_user)

    @classmethod
    async def read(cls, id_: int, session: AsyncSession) -> Optional["ViewUser"]:
        q = select(User).where(User.id == id_)
        user = await session.scalar(q)
        if user:
            return ViewUser.model_validate(user, from_attributes=True)

    @classmethod
    async def read_by_login(cls, login: str, session: AsyncSession) -> Optional["ViewUser"]:
        q = select(User).where(User.login == login)
        user = await session.scalar(q)
        if user:
            return ViewUser.model_validate(user, from_attributes=True)

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #
