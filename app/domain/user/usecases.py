import logging
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from app.domain import UserShortDto
from app.domain.common.dto.token import Token
from app.domain.user.dto.request import UserCreateRequest
from app.domain.user.dto.user import (
    UserAuthDto,
    UserDataDto,
    UserDto,
    UserFullDto,
    UsersDto, UserSignUpDto, UserVerifyDto,
)
from app.domain.user.exceptions import PasswordWrong, UserNotActive
from app.domain.user.model import UserModel
from app.infrastructure.database.exception_mapper import exception_mapper

if TYPE_CHECKING:
    from app.domain.common.usecases import Services

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def get_one(self, item_id: int) -> UserFullDto:
        model = await self.service.adapters.postgres.user.retrieve_one(item_id)
        return UserFullDto.model_validate(model)

    @exception_mapper
    async def get_many(self, **kwargs) -> UsersDto:
        skip, records, result = await self.service.adapters.postgres.user.retrieve_many(**kwargs)
        results = TypeAdapter(list[UserDto]).validate_python(result)
        return UsersDto(
            skip=skip,
            records=records,
            results=results,
        )

    @exception_mapper
    async def signin(self, auth_username: str, auth_password: str) -> Token:
        result = await self.service.adapters.postgres.user.retrieve_by_username(auth_username)
        user = UserAuthDto.model_validate(result)
        if not user.status:
            raise UserNotActive(user.user_name)
        if not self.service.security.pwd.check_pwd(auth_password, user.user_pass):
            raise PasswordWrong
        await self.service.adapters.postgres.user.update_last_login(user.id)

        return Token(
            access_token=self.service.security.jwt.create_access_token(data=user.model_dump(exclude={'user_pass'})),
            refresh_token=self.service.security.jwt.create_refresh_token(data=user.model_dump(exclude={'user_pass'})),
        )

    @exception_mapper
    async def signup(self, item: UserSignUpDto) -> UserVerifyDto:
        new_model = UserModel.create(**item.model_dump())
        new_model.user_pass = self.service.security.pwd.hash_pwd(item.user_pass)
        item_created_id = await self.service.adapters.postgres.user.create_get_id(new_model)
        item_created = await self.service.adapters.postgres.user.retrieve_by_id(item_created_id)
        return UserVerifyDto.model_validate(item_created)

    @exception_mapper
    async def verify(self, code: str) -> UserShortDto:
        item = await self.service.adapters.postgres.user.verify(code)
        return UserShortDto.model_validate(item)

    @exception_mapper
    async def create(self, item: UserCreateRequest) -> UserFullDto:
        new_model = UserModel.create(**item.model_dump())
        new_model.user_pass = self.service.security.pwd.hash_pwd(new_model.user_pass)
        item_created_id = await self.service.adapters.postgres.user.create_get_id(new_model)
        item_created = await self.service.adapters.postgres.user.retrieve_one(item_created_id)
        return UserFullDto.model_validate(item_created)

    @exception_mapper
    async def update(self, item_id: int, item_data: UserDataDto) -> UserFullDto:
        new_model = UserModel.create(**item_data.model_dump())
        await self.service.adapters.postgres.user.update(item_id, new_model)
        item_updated = await self.service.adapters.postgres.user.retrieve_one(item_id)
        return UserFullDto.model_validate(item_updated)

    @exception_mapper
    async def delete(self, item_id: int):
        await self.service.adapters.postgres.user.delete(item_id)
