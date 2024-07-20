__all__ = ["router"]

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.shared import Shared
from src.modules.auth.repository import AuthTokenRepository, AuthRepository
from src.modules.auth.schemas import RegisterData

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(data: RegisterData):
    auth_repository = Shared.f(AuthRepository)
    await auth_repository.register_user(data.name, data.login, data.password)
    return


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_repository = Shared.f(AuthRepository)
    user_id = await auth_repository.authenticate_user(password=form_data.password, login=form_data.username)
    token = AuthTokenRepository.create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}
