from fastapi import APIRouter, status

from app.controllers.http.v1.requests.permission import PermissionCreateRequest
from app.controllers.http.v1.responses.base import DeleteResultSuccess
from app.domain.permission.dto.permission import PermissionDataDto, PermissionFullDto, PermissionsDto

router = APIRouter(prefix='/permissions', tags=['Разрешения'])


@router.get(
    '',
    response_model=PermissionsDto,
    status_code=status.HTTP_200_OK,
    summary='Список разрешений',
    description='Получение списка разрешений',
)
async def get_permissions() -> PermissionsDto:
    return PermissionsDto(
        skip=0,
        records=0,
        results=[],
    )


@router.get(
    '/{item_id}',
    response_model=PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Получение информации о разрешении',
    description='Получение информации о разрешении',
)
async def get_permission(
    item_id: int,
) -> PermissionFullDto:
    return PermissionFullDto()


@router.post(
    '',
    response_model=PermissionFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создание нового разрешения',
    description='Создание нового разрешения',
)
async def create_permission(data: PermissionCreateRequest) -> PermissionFullDto:
    return PermissionFullDto()


@router.put(
    '/{item_id}',
    response_model=PermissionFullDto,
    status_code=status.HTTP_200_OK,
    summary='Изменение разрешения',
    description='Изменение разрешения',
)
async def update_permission(
    item_id: int,
    item_data: PermissionDataDto,
) -> PermissionFullDto:
    return PermissionFullDto()


@router.delete(
    '/{item_id}',
    response_model=DeleteResultSuccess,
    status_code=status.HTTP_200_OK,
    summary='Удаление разрешения',
    description='Удаление разрешения',
)
async def delete_permission(
    item_id: int,
) -> DeleteResultSuccess:
    return DeleteResultSuccess()
