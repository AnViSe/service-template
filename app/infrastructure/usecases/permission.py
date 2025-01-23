import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain.permission.dto.permission import (
    PermissionCreateRequest,
    PermissionDataDto,
    PermissionDto,
    PermissionFullDto,
    PermissionsDto,
)
from app.domain.permission.model import PermissionModel
from app.infrastructure.database.exception_mapper import exception_mapper

if TYPE_CHECKING:
    from app.infrastructure.usecases.usecases import Services

logger = logging.getLogger(__name__)


class PermissionService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def create(self, item: PermissionCreateRequest) -> PermissionFullDto:
        new_model = PermissionModel.create(**item.model_dump())
        item_created_id = await self.service.adapters.postgres.permission.create_get_id(new_model)
        item_created = await self.service.adapters.postgres.permission.retrieve_one(item_created_id)
        return PermissionFullDto.model_validate(item_created)

    @exception_mapper
    async def update(self, item_id: int, item_data: PermissionDataDto) -> PermissionFullDto:
        new_model = PermissionModel.create(**item_data.model_dump())
        await self.service.adapters.postgres.permission.update(item_id, new_model)
        item_updated = await self.service.adapters.postgres.permission.retrieve_one(item_id)
        return PermissionFullDto.model_validate(item_updated)

    @exception_mapper
    async def get_one(self, item_id: int) -> PermissionFullDto:
        model = await self.service.adapters.postgres.permission.retrieve_one(item_id)
        return PermissionFullDto.model_validate(model)

    @exception_mapper
    async def get_many(self, **kwargs) -> PermissionsDto:
        skip, records, result = await self.service.adapters.postgres.permission.retrieve_many(**kwargs)
        results = TypeAdapter(list[PermissionDto]).validate_python(result)
        return PermissionsDto(
            skip=skip,
            records=records,
            results=results,
        )

    @exception_mapper
    async def delete(self, item_id: int):
        await self.service.adapters.postgres.permission.delete(item_id)
