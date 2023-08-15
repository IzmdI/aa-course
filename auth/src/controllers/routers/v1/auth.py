from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm

from application.settings.auth import Settings as Auth_settings
from application.settings.broker import Settings as Broker_settings
from controllers.dependencies import get_current_active_user, oauth2_scheme
from controllers.stub import Stub
from db.tables import User
from dto.user import Token, UserCreateDTO, UserDTO, UserUpdateDTO
from services.user import UserService

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(Stub(UserService)),
    auth_settings: Auth_settings = Depends(Stub(Auth_settings)),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.create_access_token(auth_settings=auth_settings, data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserDTO)
async def get_self(user: User = Depends(get_current_active_user)):
    return user


@router.post("/signin")
async def sign_in(
    user_data: UserCreateDTO,
    service: UserService = Depends(Stub(UserService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.create_user(user_data, broker_settings)
    return {"signed in": "ok"}


@router.post("/login", response_model=UserDTO)
async def log_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends(Stub(UserService))
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.put("/users/{user_id}")
async def update_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_data: UserUpdateDTO,
    user_id: int = Path(),
    service: UserService = Depends(Stub(UserService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.update_user(token, user_id, user_data, broker_settings)
    return {"updated": "ok"}


@router.delete("/users/{user_id}")
async def delete_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_id: int = Path(),
    service: UserService = Depends(Stub(UserService)),
    broker_settings: Broker_settings = Depends(Stub(Broker_settings)),
):
    await service.delete_user(token, user_id, broker_settings)
    return {"deleted": "ok"}
