import logging
from typing import TYPE_CHECKING

from app.domain.auth import dto as auth_dto
from app.domain.auth.exceptions import (
    PasswordWrong,
    TokenPayload,
    TokenPayloadUser,
    TokenPayloadUserId,
    UserMailNotVerified, UserNotActive,
)
from app.domain.user.model import UserModel
from app.infrastructure.database import exception_mapper

if TYPE_CHECKING:
    from app.infrastructure.usecases.usecases import Services

logger = logging.getLogger('service.auth')


class AuthService:

    def __init__(self, service: 'Services'):
        self.service = service

    @exception_mapper
    async def signin(self, auth_username: str, auth_password: str) -> auth_dto.Token:
        user = await self.service.adapters.postgres.auth.get_auth_by_username(auth_username)
        if not user.status:
            raise UserNotActive(user.user_name)
        if not self.service.security.pwd.check_pwd(auth_password, user.user_pass):
            raise PasswordWrong
        await self.service.adapters.postgres.auth.update_last_login(user.id)

        return auth_dto.Token(
            access_token=self.service.security.jwt.create_access_token(data=user.model_dump(exclude={'user_pass'})),
            refresh_token=self.service.security.jwt.create_refresh_token(),
        )

    @exception_mapper
    async def signup(self, item: auth_dto.SignUpRequest) -> auth_dto.SignUpDto:
        new_model = UserModel.create(**item.model_dump())
        new_model.user_pass = self.service.security.pwd.hash_pwd(item.user_pass)
        item_created_id = await self.service.adapters.postgres.user.create_get_id(new_model)
        item_created = await self.service.adapters.postgres.auth.get_signup_by_id(item_created_id)
        await self.service.adapters.bus.publish(item_created, 'user_signed')
        return item_created

    @exception_mapper
    async def verify(self, code: str) -> auth_dto.VerifyDto:
        return await self.service.adapters.postgres.auth.verify_by_code(code)

    @exception_mapper
    async def change_password(self, user_id: int, password: str) -> None:
        hashed_password = self.service.security.pwd.hash_pwd(password)
        await self.service.adapters.postgres.auth.update_password(user_id, hashed_password)

    @exception_mapper
    async def reset_password(self, email: str) -> None:
        user = await self.service.adapters.postgres.auth.get_reset_by_email(email)
        if not user.status:
            raise UserNotActive(user.user_name)
        if user.verification_code and user.dt_ac is None:
            raise UserMailNotVerified(email)
        await self.service.adapters.postgres.auth.reset_password(user.id)

    @exception_mapper
    async def update_password(self, code: str, password: str) -> None:
        user = await self.service.adapters.postgres.auth.verify_by_code(code)
        await self.service.adapters.postgres.auth.update_password(user.id, password)

    @exception_mapper
    async def current_user_by_token(self, token: str) -> auth_dto.AuthDto:
        if (payload := self.service.security.jwt.decode_access_token(token)) is None:
            raise TokenPayload
        if (data := payload.get('user')) is None:
            raise TokenPayloadUser
        if (ident := data.get('id')) is None:
            raise TokenPayloadUserId
        if (user := await self.service.adapters.postgres.auth.get_auth_by_id(ident)) is not None:
            return user
