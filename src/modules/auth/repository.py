__all__ = ["AuthTokenRepository", "AuthRepository"]

from datetime import timedelta, datetime
from typing import Optional

from authlib.jose import jwt, JoseError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ObjectNotFound
from src.api.shared import Shared
from src.config import settings
from src.modules.auth.exceptions import IncorrectCredentialsException
from src.modules.auth.exceptions import UserAlreadyRegisteredException
from src.modules.auth.schemas import VerificationResult, UserCredentialsFromDB
from src.modules.user.repository import UserRepository
from src.modules.user.schemas import ViewUser, CreateUser, AuthorizedUserInfo
from src.storages.sqlalchemy.models import User


class AuthTokenRepository:
    ALGORITHM = "RS256"

    @classmethod
    async def verify_access_token(cls, auth_token: str, session: AsyncSession) -> VerificationResult:
        try:
            payload = jwt.decode(auth_token, settings.jwt_private_key.get_secret_value())
        except JoseError:
            return VerificationResult(success=False)

        user_repository = Shared.f(UserRepository)
        user_id: str = payload.get("sub")

        if user_id is None or not user_id.isdigit():
            return VerificationResult(success=False)

        user: ViewUser | None = await user_repository.read(int(user_id), session)
        if user is None:
            return VerificationResult(success=False)

        return VerificationResult(success=True, user=AuthorizedUserInfo.model_validate(user, from_attributes=True))

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        access_token = cls._create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=1),
        )
        return access_token

    @classmethod
    def _create_access_token(cls, data: dict, expires_delta: timedelta) -> str:
        payload = data.copy()
        issued_at = datetime.utcnow()
        expire = issued_at + expires_delta
        payload.update({"exp": expire, "iat": issued_at})
        encoded_jwt = jwt.encode({"alg": cls.ALGORITHM}, payload, settings.jwt_private_key.get_secret_value())
        return str(encoded_jwt, "utf-8")


class AuthRepository:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"])

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)

    @classmethod
    async def register_user(cls, name: str, login: str, password: str) -> int:
        async with Shared.f(AsyncSession) as session:
            user_repository = Shared.f(UserRepository)
            user = await user_repository.read_by_login(login, session)
            if user is not None:
                raise UserAlreadyRegisteredException()

            user = await user_repository.create(
                CreateUser(login=login, password_hash=cls.get_password_hash(password), name=name), session
            )
            return user.id

    @classmethod
    async def authenticate_user(cls, login: str, password: str) -> int:
        user_credentials = await cls._get_user(login)
        if user_credentials is None:
            raise ObjectNotFound()
        password_verified = await cls.verify_password(password, user_credentials.password_hash)
        if not password_verified:
            raise IncorrectCredentialsException()
        return user_credentials.user_id

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.PWD_CONTEXT.verify(plain_password, hashed_password)

    @classmethod
    async def _get_user(cls, login: str) -> Optional[UserCredentialsFromDB]:
        from src.api.shared import Shared

        async with Shared.f(AsyncSession) as session:
            q = select(User.id, User.password_hash).where(login == User.login)
            user = (await session.execute(q)).one_or_none()
            if user:
                return UserCredentialsFromDB(
                    user_id=user.id,
                    password_hash=user.password_hash,
                )
