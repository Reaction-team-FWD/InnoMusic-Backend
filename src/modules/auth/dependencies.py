from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shared import Shared
from src.modules.auth.exceptions import NoCredentialsException, IncorrectCredentialsException
from src.modules.auth.repository import AuthTokenRepository
from src.modules.user.schemas import AuthorizedUserInfo

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="Bearer",
    description="Your JSON Web Token (JWT)",
    auto_error=False,  # We'll handle error manually
)


async def verify_request(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> AuthorizedUserInfo:
    """
    Check one of the following:
    - Bearer token from header with BOT_TOKEN
    - Bearer token from header with webapp data
    :raises NoCredentialsException: if token is not provided
    :raises IncorrectCredentialsException: if token is invalid
    """

    if not token or token == "undefined":
        raise NoCredentialsException()

    async with Shared.f(AsyncSession) as session:
        verification_result = await AuthTokenRepository.verify_access_token(token, session)

    if verification_result.success:
        return verification_result.user

    raise IncorrectCredentialsException()


VerifiedDep = Annotated[AuthorizedUserInfo, Depends(verify_request)]

__all__ = ["verify_request", "VerifiedDep"]
