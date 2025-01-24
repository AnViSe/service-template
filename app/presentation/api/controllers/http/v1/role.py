import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, status

from app.domain.role import dto as role_dto
from app.infrastructure.usecases import Services
from .helper import QueryParams
from .responses.base import BaseErrorResponse, DeleteResultSuccess
from ..deps import CurrentUserAuth

logger = logging.getLogger('http.v1.role')

router = APIRouter(
    prefix='/roles',
    tags=['Роли'],
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': BaseErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': BaseErrorResponse},
        status.HTTP_409_CONFLICT: {'model': BaseErrorResponse},
    },
)


@router.get(
    '',
    response_model=role_dto.RolesDto,
    status_code=status.HTTP_200_OK,
    summary='Список ролей',
    description='Получение списка ролей',
)
@inject
async def get_roles(
    service: FromDishka[Services],
    query: QueryParams = Depends(),
) -> role_dto.RolesDto:
    return await service.role.get_many(**query.model_dump())


@router.get(
    '/{item_id}',
    response_model=role_dto.RoleFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о роли',
    description='Получение информации о роли',
)
@inject
async def get_role(
    item_id: int,
    service: FromDishka[Services],
) -> role_dto.RoleFullDto:
    return await service.role.get_one(item_id)


@router.post(
    '',
    response_model=role_dto.RoleFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание новой роли',
    description='Создание новой роли',
)
@inject
async def create_role(
    data: role_dto.RoleCreateRequest,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> role_dto.RoleFullDto:
    return await service.role.create(data, user.id)


@router.put(
    '/{item_id}',
    response_model=role_dto.RoleFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение роли',
    description='Изменение роли',
)
@inject
async def update_role(
    item_id: int,
    item_data: role_dto.RoleDataDto,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> role_dto.RoleFullDto:
    return await service.role.update(item_id, item_data, user.id)


@router.delete(
    '/{item_id}',
    response_model=DeleteResultSuccess,
    status_code=status.HTTP_200_OK,
    summary='Удаление роли',
    description='Удаление роли',
)
@inject
async def delete_role(
    item_id: int,
    user: CurrentUserAuth,
    service: FromDishka[Services],
) -> DeleteResultSuccess:
    await service.role.delete(item_id, user.id)
    return DeleteResultSuccess(detail={'id': item_id})
