import logging
from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.auth import dto as auth_dto
from app.domain.auth.exceptions import VerificationCodeNotFound
from app.domain.user.exceptions import UserIdNotFound, UserMailNotFound, UserNameNotFound
from app.infrastructure.database.models.user import UserDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.auth')


class AuthRepository(BaseRepository[UserDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=UserDB, session_maker=session_maker)

    async def get_auth_by_id(self, user_id: int) -> auth_dto.AuthDto:
        sql = (
            select(
                UserDB.id,
                UserDB.user_name,
                UserDB.user_pass,
                UserDB.user_mail,
                UserDB.sd_id,
                UserDB.status,
            )
            .where(
                UserDB.id == user_id
                )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise UserIdNotFound(user_id)
            return auth_dto.AuthDto.model_validate(item)

    async def get_auth_by_username(self, user_name: str) -> auth_dto.AuthDto:
        sql = (
            select(
                UserDB.id,
                UserDB.user_name,
                UserDB.user_pass,
                UserDB.user_mail,
                UserDB.sd_id,
                UserDB.status,
            )
            .where(
                and_(func.lower(UserDB.user_name) == user_name.lower())
            )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise UserNameNotFound(user_name)
            return auth_dto.AuthDto.model_validate(item)

    async def get_reset_by_email(self, email: str) -> auth_dto.ResetDto:
        sql = (
            select(
                UserDB.id,
                UserDB.verification_code,
                UserDB.dt_ac,
                UserDB.status,
            )
            .where(
                and_(func.lower(UserDB.user_mail) == email.lower())
            )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise UserMailNotFound(email)
            return auth_dto.ResetDto.model_validate(item)

    async def get_signup_by_id(self, user_id: int) -> auth_dto.SignUpDto:
        sql = (
            select(
                UserDB.id,
                UserDB.user_name,
                UserDB.user_mail,
                UserDB.verification_code,
                UserDB.status,
            )
            .where(
                and_(UserDB.id == user_id)
            )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise UserIdNotFound(user_id)
            return auth_dto.SignUpDto.model_validate(item)

    async def get_verify_by_code(self, code: str) -> auth_dto.VerifyDto:
        sql = (
            select(
                UserDB.id,
                UserDB.user_name,
            )
            .where(
                and_(UserDB.verification_code == code)
            )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise VerificationCodeNotFound
            return auth_dto.VerifyDto.model_validate(item)

    async def update_last_login(self, user_id: int) -> None:
        sql = (
            update(UserDB)
            .where(UserDB.id == user_id)
            .values(last_login=datetime.now())
            .returning(UserDB.id)
        )
        async with self.session_maker() as session:
            item = await session.scalar(sql)
            if not item:
                raise UserIdNotFound(user_id)
            await session.flush()
            await session.commit()

    async def update_password(self, user_id: int, password: str) -> None:
        sql = (
            update(UserDB)
            .where(UserDB.id == user_id)
            .values(
                user_pass=password,
                verification_code=None,
                dt_up=datetime.now(),
            )
            .returning(UserDB.id)
        )
        async with self.session_maker() as session:
            item = await session.scalar(sql)
            if not item:
                raise UserIdNotFound(user_id)
            await session.flush()
            await session.commit()

    async def reset_password(self, user_id: int) -> None:
        sql = (
            update(UserDB)
            .where(UserDB.id == user_id)
            .values(
                verification_code=token_urlsafe(70),
                dt_up=datetime.now(),
            )
            .returning(UserDB.id)
        )
        async with self.session_maker() as session:
            item = await session.scalar(sql)
            if not item:
                raise UserIdNotFound(user_id)
            await session.flush()
            await session.commit()

    async def verify_by_code(self, code: str) -> auth_dto.VerifyDto:
        sql = (
            update(UserDB)
            .where(UserDB.verification_code == code)
            .values(
                dt_ac=datetime.now(),
                dt_up=datetime.now(),
                verification_code=None,
                status=True,
            )
            .returning(
                UserDB.id,
                UserDB.user_name,
                UserDB.user_desc,
                UserDB.status,
            )
        )
        async with self.session_maker() as session:
            _exec = await session.execute(sql)
            item = _exec.mappings().one_or_none()
            if item is None:
                raise VerificationCodeNotFound
            await session.flush()
            await session.commit()
            return auth_dto.VerifyDto.model_validate(item)
