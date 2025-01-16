import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain.permission.dto.permission import (
    PermissionDataDto,
    PermissionDto,
    PermissionFullDto,
    PermissionsDto,
    PermissionUpdateDto,
)
from app.domain.permission.model import PermissionModel

if TYPE_CHECKING:
    from app.domain.common.usecases import Services

logger = logging.getLogger(__name__)

class PermissionService:

    def __init__(self, service: 'Services'):
        self.service = service

    async def create(self, item: PermissionDataDto) -> PermissionFullDto:
        new_model = PermissionModel.create(**item.model_dump())
        item_created_id = await self.service.adapters.postgres.permission.create_get_id(new_model)
        item_created = await self.service.adapters.postgres.permission.retrieve_one(item_created_id)
        return PermissionFullDto.model_validate(item_created)

    async def update(self, item: PermissionUpdateDto) -> PermissionFullDto:
        new_model = PermissionModel.create(**item.update_data.model_dump(), id=item.id)
        await self.service.adapters.postgres.permission.update(item.id, new_model)
        item_updated = await self.service.adapters.postgres.permission.retrieve_one(item.id)
        return PermissionFullDto.model_validate(item_updated)

    async def get_one(self, permission_id: int) -> PermissionFullDto:
        model = await self.service.adapters.postgres.permission.retrieve_one(permission_id)
        return PermissionFullDto.model_validate(model)

    async def get_many(self, **kwargs) -> PermissionsDto:
        skip, records, result = await self.service.adapters.postgres.permission.retrieve_many(**kwargs)
        results = TypeAdapter(list[PermissionDto]).validate_python(result)
        return PermissionsDto(
            skip=skip,
            records=records,
            results=results,
        )

    async def delete(self, permission_id: int):
        await self.service.adapters.postgres.permission.delete(permission_id)
