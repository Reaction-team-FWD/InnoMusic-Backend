__all__ = ["UserRepository"]

from typing import Optional

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.schemas import ViewUser, CreateUser
from src.modules.utils import get_available_ids
from src.storages.sqlalchemy.models.user import User


class UserRepository:
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list["ViewUser"]:
        users = await session.scalars(select(User))
        return [ViewUser.model_validate(user, from_attributes=True) for user in users]

    # ------------------ CRUD ------------------ #

    @classmethod
    async def create(cls, user: CreateUser, session: AsyncSession) -> ViewUser:
        user_dict = user.model_dump()
        user_dict["id"] = await get_available_ids(session, User)
        if user_dict.get("name") is None:
            user_dict["name"] = user_dict["login"]
        new_user = await session.scalar(insert(User).values(user_dict).returning(User))
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
        user = await session.scalar(select(User).where(id_ == User.id))
        if user:
            return ViewUser.model_validate(user, from_attributes=True)

    @classmethod
    async def read_by_login(cls, login: str, session: AsyncSession) -> Optional["ViewUser"]:
        user = await session.scalar(select(User).where(login == User.login))
        if user:
            return ViewUser.model_validate(user, from_attributes=True)

    @classmethod
    async def delete(cls, id_: int, session: AsyncSession) -> None:
        await session.execute(delete(User).where(id_ == User.id))
        await session.commit()

    # ^^^^^^^^^^^^^^^^^^^ CRUD ^^^^^^^^^^^^^^^^^^^ #
