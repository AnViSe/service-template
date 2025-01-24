import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain.user import dto as user_dto
from app.domain.user.model import UserModel
from app.infrastructure.database import exception_mapper

if TYPE_CHECKING:
    from app.infrastructure.usecases.usecases import Services

logger = logging.getLogger('service.user')


class UserService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def get_one(self, item_id: int) -> user_dto.UserFullDto:
        return await self.service.adapters.postgres.user.get_full_by_id(item_id)

    @exception_mapper
    async def get_many(self, **kwargs) -> user_dto.UsersDto:
        skip, records, result = await self.service.adapters.postgres.user.get_many(**kwargs)
        results = TypeAdapter(list[user_dto.UserDto]).validate_python(result)
        return user_dto.UsersDto(
            skip=skip,
            records=records,
            results=results,
        )

    @exception_mapper
    async def create(
        self,
        item: user_dto.UserCreateRequest,
        owner_id: int | None = None,
    ) -> user_dto.UserFullDto:
        new_model = UserModel.create(**item.model_dump())
        new_model.user_pass = self.service.security.pwd.hash_pwd(new_model.user_pass)
        item_created_id = await self.service.adapters.postgres.user.create_get_id(new_model, owner_id)
        item_created = await self.service.adapters.postgres.user.get_full_by_id(item_created_id)
        await self.service.adapters.bus.publish('user_created', item_created)
        return item_created

    @exception_mapper
    async def update(
        self,
        item_id: int,
        item_data: user_dto.UserDataDto,
        owner_id: int | None = None,
    ) -> user_dto.UserFullDto:
        new_model = UserModel.create(**item_data.model_dump())
        await self.service.adapters.postgres.user.update(item_id, new_model, owner_id)
        item_updated = await self.service.adapters.postgres.user.get_full_by_id(item_id)
        await self.service.adapters.bus.publish('user_updated', item_updated)
        return item_updated

    @exception_mapper
    async def delete(
        self,
        item_id: int,
        owner_id: int | None = None,
    ) -> None:
        await self.service.adapters.postgres.user.delete(item_id, owner_id)
        await self.service.adapters.bus.publish('user_deleted', item_id)
