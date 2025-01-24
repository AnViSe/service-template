import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain.role import dto as role_dto
from app.domain.role.model import RoleModel
from app.infrastructure.database.exception_mapper import exception_mapper

if TYPE_CHECKING:
    from app.infrastructure.usecases.usecases import Services

logger = logging.getLogger(__name__)


class RoleService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def get_one(self, item_id: int) -> role_dto.RoleFullDto:
        return await self.service.adapters.postgres.role.get_full_by_id(item_id)

    @exception_mapper
    async def get_many(self, **kwargs) -> role_dto.RolesDto:
        skip, records, result = await self.service.adapters.postgres.role.get_many(**kwargs)
        results = TypeAdapter(list[role_dto.RoleDto]).validate_python(result)
        return role_dto.RolesDto(
            skip=skip,
            records=records,
            results=results,
        )

    @exception_mapper
    async def create(
        self,
        item: role_dto.RoleCreateRequest,
        owner_id: int | None = None,
    ) -> role_dto.RoleFullDto:
        new_model = RoleModel.create(**item.model_dump())
        item_created_id = await self.service.adapters.postgres.role.create_get_id(new_model, owner_id)
        item_created = await self.service.adapters.postgres.role.get_full_by_id(item_created_id)
        await self.service.adapters.bus.publish('role_created', item_created)
        return item_created

    @exception_mapper
    async def update(
        self, item_id:
        int, item_data: role_dto.RoleDataDto,
        owner_id: int | None = None,
    ) -> role_dto.RoleFullDto:
        new_model = RoleModel.create(**item_data.model_dump())
        await self.service.adapters.postgres.role.update(item_id, new_model, owner_id)
        item_updated = await self.service.adapters.postgres.role.get_full_by_id(item_id)
        await self.service.adapters.bus.publish('role_updated', item_updated)
        return item_updated

    @exception_mapper
    async def delete(
        self,
        item_id: int,
        owner_id: int | None = None,
    ) -> None:
        await self.service.adapters.postgres.role.delete(item_id, owner_id)
        await self.service.adapters.bus.publish('role_deleted', item_id)
