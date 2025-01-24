import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain.permission import dto as perm_dto
from app.domain.permission.model import PermissionModel
from app.infrastructure.database.exception_mapper import exception_mapper

if TYPE_CHECKING:
    from app.infrastructure.usecases.usecases import Services

logger = logging.getLogger(__name__)


class PermissionService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def get_one(self, item_id: int) -> perm_dto.PermissionFullDto:
        return await self.service.adapters.postgres.permission.get_full_by_id(item_id)

    @exception_mapper
    async def get_many(self, **kwargs) -> perm_dto.PermissionsDto:
        skip, records, result = await self.service.adapters.postgres.permission.get_many(**kwargs)
        results = TypeAdapter(list[perm_dto.PermissionDto]).validate_python(result)
        return perm_dto.PermissionsDto(
            skip=skip,
            records=records,
            results=results,
        )

    @exception_mapper
    async def create(
        self,
        item: perm_dto.PermissionCreateRequest,
        owner_id: int | None = None,
    ) -> perm_dto.PermissionFullDto:
        new_model = PermissionModel.create(**item.model_dump())
        item_created_id = await self.service.adapters.postgres.permission.create_get_id(new_model, owner_id)
        item_created = await self.service.adapters.postgres.permission.get_full_by_id(item_created_id)
        await self.service.adapters.bus.publish('permission_created', item_created)
        return item_created

    @exception_mapper
    async def update(
        self, item_id:
        int, item_data: perm_dto.PermissionDataDto,
        owner_id: int | None = None,
    ) -> perm_dto.PermissionFullDto:
        new_model = PermissionModel.create(**item_data.model_dump())
        await self.service.adapters.postgres.permission.update(item_id, new_model, owner_id)
        item_updated = await self.service.adapters.postgres.permission.get_full_by_id(item_id)
        await self.service.adapters.bus.publish('permission_updated', item_updated)
        return item_updated

    @exception_mapper
    async def delete(
        self,
        item_id: int,
        owner_id: int | None = None,
    ) -> None:
        await self.service.adapters.postgres.permission.delete(item_id, owner_id)
        await self.service.adapters.bus.publish('permission_deleted', item_id)
