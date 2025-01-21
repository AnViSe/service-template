import logging
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.domain import UserShortDto
from app.domain.common.dto.token import Token
from app.domain.common.usecases import Services
from app.domain.user.dto.request import UserSignUpRequest
from app.presentation.api.controllers.http.v1.responses.auth import UserSignUpResponse

router = APIRouter(tags=['Авторизация'])

logger = logging.getLogger('http.v1.auth')


@router.post(
    '/signin',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Авторизация пользователя',
    description='Авторизация пользователя',
)
@inject
async def signin(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[Services],
):
    return await service.user.signin(auth_username=data.username, auth_password=data.password)


@router.post(
    '/signup',
    response_model=UserSignUpResponse,
    status_code=status.HTTP_200_OK,
    summary='Регистрация пользователя',
    description='Регистрация пользователя',
)
@inject
async def signup(
    data: UserSignUpRequest,
    service: FromDishka[Services],
):
    return await service.user.signup(data)


@router.get(
    '/verify/{code}',
    response_model=UserShortDto,
    status_code=status.HTTP_200_OK,
    summary='Проверка кода регистрации',
    description='Проверка кода регистрации',
)
@inject
async def verify(
    code: str,
    service: FromDishka[Services],
):
    return await service.user.verify(code)
