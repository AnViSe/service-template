import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.domain.common.usecases import Services
from app.domain.user.dto.request import UserCreateRequest
from app.domain.user.dto.user import (
    UserDataDto,
    UserFullDto,
    UsersDto,
)
from .responses.base import DeleteResultSuccess
from ..handlers.helper import QueryParams

router = APIRouter(prefix='/users', tags=['Пользователи'])

logger = logging.getLogger('http.v1.user')


@router.get(
    '',
    response_model=UsersDto,
    status_code=status.HTTP_200_OK,
    summary='Список пользователей',
    description='Получение списка пользователей',
)
@inject
async def get_users(
    service: FromDishka[Services],
    query: QueryParams = Depends(),
) -> UsersDto:
    return await service.user.get_many(**query.model_dump())


@router.get(
    '/{item_id}',
    response_model=UserFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о пользователе',
    description='Получение информации о пользователе',
)
@inject
async def get_user(
    item_id: int,
    service: FromDishka[Services],
) -> UserFullDto:
    return await service.user.get_one(item_id)


@router.post(
    '',
    response_model=UserFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового пользователя',
    description='Создание нового пользователя',
)
@inject
async def create_user(
    data: UserCreateRequest,
    service: FromDishka[Services],
) -> UserFullDto:
    return await service.user.create(data)


@router.put(
    '/{item_id}',
    response_model=UserFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение пользователя',
    description='Изменение пользователя',
)
@inject
async def update_user(
    item_id: int,
    item_data: UserDataDto,
    service: FromDishka[Services],
) -> UserFullDto:
    return await service.user.update(item_id, item_data)


@router.delete(
    '/{item_id}',
    response_model=DeleteResultSuccess,
    status_code=status.HTTP_200_OK,
    summary='Удаление пользователя',
    description='Удаление пользователя',
)
@inject
async def delete_user(
    item_id: int,
    service: FromDishka[Services],
) -> DeleteResultSuccess:
    await service.user.delete(item_id)
    return DeleteResultSuccess(detail={'id': item_id})
