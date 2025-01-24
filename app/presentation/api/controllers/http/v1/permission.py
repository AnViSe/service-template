import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.domain.permission import dto as perm_dto
from app.infrastructure.usecases import Services
from .helper import QueryParams
from .responses.base import BaseErrorResponse, DeleteResultSuccess
from ..deps import CurrentUserAuth

logger = logging.getLogger('http.v1.permission')

router = APIRouter(
    prefix='/permissions',
    tags=['Разрешения'],
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': BaseErrorResponse},
        status.HTTP_409_CONFLICT: {'model': BaseErrorResponse},
    },
)


@router.get(
    '',
    response_model=perm_dto.PermissionsDto,
    status_code=status.HTTP_200_OK,
    summary='Список разрешений',
    description='Получение списка разрешений',
)
@inject
async def get_permissions(
    service: FromDishka[Services],
    query: QueryParams = Depends(),
) -> perm_dto.PermissionsDto:
    return await service.permission.get_many(**query.model_dump())


@router.get(
    '/{item_id}',
    response_model=perm_dto.PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о разрешении',
    description='Получение информации о разрешении',
)
@inject
async def get_permission(
    item_id: int,
    service: FromDishka[Services],
) -> perm_dto.PermissionFullDto:
    return await service.permission.get_one(item_id)


@router.post(
    '',
    response_model=perm_dto.PermissionFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового разрешения',
    description='Создание нового разрешения',
)
@inject
async def create_permission(
    data: perm_dto.PermissionCreateRequest,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> perm_dto.PermissionFullDto:
    return await service.permission.create(data, user.id)


@router.put(
    '/{item_id}',
    response_model=perm_dto.PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение разрешения',
    description='Изменение разрешения',
)
@inject
async def update_permission(
    item_id: int,
    item_data: perm_dto.PermissionDataDto,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> perm_dto.PermissionFullDto:
    return await service.permission.update(item_id, item_data, user.id)


@router.delete(
    '/{item_id}',
    response_model=DeleteResultSuccess,
    status_code=status.HTTP_200_OK,
    summary='Удаление разрешения',
    description='Удаление разрешения',
)
@inject
async def delete_permission(
    item_id: int,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> DeleteResultSuccess:
    await service.permission.delete(item_id, user.id)
    return DeleteResultSuccess(detail={'id': item_id})
