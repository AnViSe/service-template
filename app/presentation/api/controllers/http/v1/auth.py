import logging
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.domain.auth import dto as auth_dto
from app.domain.auth.exceptions import PasswordWrong
from app.infrastructure.usecases.usecases import Services
from ..deps import CurrentUser

router = APIRouter(tags=['Авторизация'])

logger = logging.getLogger('http.v1.auth')


@router.post(
    '/signin',
    response_model=auth_dto.Token,
    status_code=status.HTTP_200_OK,
    summary='Авторизация пользователя',
    description='Авторизация пользователя',
)
@inject
async def signin(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[Services],
):
    return await service.auth.signin(auth_username=data.username, auth_password=data.password)


@router.post(
    '/signup',
    response_model=auth_dto.SignUpDto,
    status_code=status.HTTP_200_OK,
    summary='Регистрация пользователя',
    description='Регистрация пользователя',
)
@inject
async def signup(
    data: auth_dto.SignUpRequest,
    service: FromDishka[Services],
):
    return await service.auth.signup(data)


@router.get(
    '/verify/{code}',
    response_model=auth_dto.VerifyDto,
    status_code=status.HTTP_200_OK,
    summary='Проверка кода регистрации',
    description='Проверка кода регистрации',
)
@inject
async def verify(
    code: str,
    service: FromDishka[Services],
):
    return await service.auth.verify(code)


@router.get(
    '/refresh/{token}',
    response_model=auth_dto.Token,
    status_code=status.HTTP_200_OK,
    summary='Обновление токена доступа',
    description='Обновление токена доступа',
)
@inject
async def refresh_token(
    token: str,
    service: FromDishka[Services],
):
    access_token = service.security.jwt.refresh_access_token(token)
    return auth_dto.Token(
        access_token=access_token,
        refresh_token=token,
    )


@router.post(
    '/password/change',
    response_model=auth_dto.UpdatePasswordSuccess,
    status_code=status.HTTP_200_OK,
    summary='Изменение пароля',
    description='Изменение пароля',
)
@inject
async def password_change(
    passwords: auth_dto.PasswordChangeRequest,
    user: CurrentUser,
    service: FromDishka[Services],
):
    if service.security.pwd.check_pwd(passwords.password_old, user.user_pass):
        await service.auth.change_password(user.id, passwords.password_new)
        return auth_dto.UpdatePasswordSuccess(info={'user_name': user.user_name})
    else:
        raise PasswordWrong


@router.get(
    '/password/reset/{email}',
    response_model=auth_dto.ResetPasswordEmailSent,
    status_code=status.HTTP_200_OK,
    summary='Запрос на сброс пароля по email',
    description='Запрос на сброс пароля по email',
)
@inject
async def password_reset(
    email: str,
    service: FromDishka[Services],
):
    await service.auth.reset_password(email)
    return auth_dto.ResetPasswordEmailSent(info={'user_mail': email})


@router.post(
    '/password/update/{code}',
    response_model=auth_dto.UpdatePasswordSuccess,
    status_code=status.HTTP_200_OK,
    summary='Обновление пароля',
    description='Обновление пароля',
)
@inject
async def password_update(
    code: str,
    passwords: auth_dto.PasswordUpdateRequest,
    service: FromDishka[Services],
):
    await service.auth.update_password(code, passwords.user_pass)
    return auth_dto.UpdatePasswordSuccess
