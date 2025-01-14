from fastapi import APIRouter, status

from app.domain.permission.dto.permission import PermissionsDTO

router = APIRouter(prefix='/permissions', tags=['Разрешения'])


@router.get(
    '',
    response_model=PermissionsDTO,
    status_code=status.HTTP_200_OK,
    summary='Список разрешений',
    description='Получение списка разрешений',
)
async def get_permissions() -> PermissionsDTO:
    return PermissionsDTO(
        skip=0,
        records=0,
        results=[],
    )
