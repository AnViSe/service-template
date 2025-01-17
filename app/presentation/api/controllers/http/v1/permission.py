import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.domain.common.usecases import Services
from app.domain.permission.dto.permission import (
    PermissionCreateRequest,
    PermissionDataDto,
    PermissionFullDto,
    PermissionsDto,
)
from .responses.base import DeleteResultSuccess
from ..handlers.helper import QueryParams

router = APIRouter(prefix='/permissions', tags=['Разрешения'])

logger = logging.getLogger('http.v1.permission')


@router.get(
    '',
    response_model=PermissionsDto,
    status_code=status.HTTP_200_OK,
    summary='Список разрешений',
    description='Получение списка разрешений',
)
@inject
async def get_permissions(
    service: FromDishka[Services],
    query: QueryParams = Depends(),
) -> PermissionsDto:
    return await service.permission.get_many(**query.model_dump())


@router.get(
    '/{item_id}',
    response_model=PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о разрешении',
    description='Получение информации о разрешении',
)
@inject
async def get_permission(
    item_id: int,
    service: FromDishka[Services],
) -> PermissionFullDto:
    return await service.permission.get_one(item_id)


@router.post(
    '',
    response_model=PermissionFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового разрешения',
    description='Создание нового разрешения',
)
@inject
async def create_permission(
    data: PermissionCreateRequest,
    service: FromDishka[Services],
) -> PermissionFullDto:
    return await service.permission.create(data)


@router.put(
    '/{item_id}',
    response_model=PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение разрешения',
    description='Изменение разрешения',
)
@inject
async def update_permission(
    item_id: int,
    item_data: PermissionDataDto,
    service: FromDishka[Services],
) -> PermissionFullDto:
    return await service.permission.update(item_id, item_data)


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
    service: FromDishka[Services],
) -> DeleteResultSuccess:
    await service.permission.delete(item_id)
    return DeleteResultSuccess(detail={'id': item_id})
