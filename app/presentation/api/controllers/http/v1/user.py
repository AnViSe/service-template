import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.domain.user import dto as user_dto
from app.infrastructure.usecases import Services
from .helper import QueryParams
from .responses.base import BaseErrorResponse, DeleteResultSuccess
from ..deps import CurrentUserAuth, CurrentUserFull, CurrentUserPermissions, CurrentUserRoles

logger = logging.getLogger('http.v1.user')

router = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': BaseErrorResponse},
        status.HTTP_409_CONFLICT: {'model': BaseErrorResponse},
    },
)


@router.get(
    '',
    response_model=user_dto.UsersDto,
    status_code=status.HTTP_200_OK,
    summary='Список пользователей',
    description='Получение списка пользователей',
)
@inject
async def get_users(
    service: FromDishka[Services],
    query: QueryParams = Depends(),
) -> user_dto.UsersDto:
    return await service.user.get_many(**query.model_dump())


@router.get(
    '/me',
    response_model=user_dto.UserFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о текущем пользователе',
    description='Получение информации о текущем пользователе',
)
@inject
async def get_user_me(
    user: CurrentUserFull,
) -> user_dto.UserFullDto:
    return user


@router.get(
    '/me/roles',
    response_model=list[str],
    status_code=status.HTTP_200_OK,
    summary='Получение информации о ролях текущего пользователя',
    description='Получение информации о ролях текущего пользователя',
)
@inject
async def get_user_me_roles(
    roles: CurrentUserRoles,
):
    return roles


@router.get(
    '/me/permissions',
    response_model=list[str],
    summary='Получение информации о разрешениях текущего пользователя',
    description='Получение информации о разрешениях текущего пользователя',
)
async def get_user_me_permissions(
    permissions: CurrentUserPermissions,
):
    return permissions


@router.get(
    '/{item_id}',
    response_model=user_dto.UserFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о пользователе',
    description='Получение информации о пользователе',
)
@inject
async def get_user(
    item_id: int,
    service: FromDishka[Services],
) -> user_dto.UserFullDto:
    return await service.user.get_one(item_id)


@router.post(
    '',
    response_model=user_dto.UserFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового пользователя',
    description='Создание нового пользователя',
)
@inject
async def create_user(
    data: user_dto.UserCreateRequest,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> user_dto.UserFullDto:
    return await service.user.create(data, user.id)


@router.put(
    '/{item_id}',
    response_model=user_dto.UserFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение пользователя',
    description='Изменение пользователя',
)
@inject
async def update_user(
    item_id: int,
    item_data: user_dto.UserDataDto,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> user_dto.UserFullDto:
    return await service.user.update(item_id, item_data, user.id)


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
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> DeleteResultSuccess:
    await service.user.delete(item_id, user.id)
    return DeleteResultSuccess(detail={'id': item_id})
