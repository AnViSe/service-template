import logging
from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.common.exceptions.base import NotFoundException
from app.domain.user.exceptions import (
    UserIdAlreadyExists,
    UserIdNotFound,
    UserMailAlreadyExists,
    UserNameAlreadyExists,
    UserNameNotFound,
)
from app.domain.user.model import UserModel
from app.infrastructure.database.models.user import UserDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.user')


class UserRepository(BaseRepository[UserDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=UserDB, session_maker=session_maker)

    async def retrieve_by_id(self, item_id: int | None = None) -> UserDB | None:
        try:
            return await self.retrieve_one(item_id)
        except IdNotFoundException as e:
            raise UserIdNotFound(item_id) from e

    async def retrieve_by_username(self, user_name: str) -> UserDB | None:
        try:
            return await self.retrieve_one(
                where_clause=[func.lower(self.database_model.user_name) == user_name.lower()]
            )
        except NotFoundException as e:
            raise UserNameNotFound(user_name) from e

    async def retrieve_by_code(self, code: str) -> UserDB | None:
        return await self.retrieve_one(
            where_clause=[self.database_model.verification_code == code]
        )

    async def verify(self, code: str):
        sql = (
            update(UserDB)
            .where(UserDB.verification_code == code)
            .values(
                dt_ac=datetime.now(),
                dt_up=datetime.now(),
                verification_code=None,
                status=True,
            )
            .returning(UserDB.id, UserDB.user_name, UserDB.user_desc, UserDB.status)
        )
        async with self.session_maker.begin() as session:
            item = (await session.scalars(sql)).one_or_none()
            if not item:
                raise NotFoundException
            await session.flush()
            return item

    async def retrieve_many(self, **kwargs):
        self.order_fields = [f'{UserDB.__tablename__}.id']

        sql = (
            select(
                UserDB.id,
                UserDB.user_name,
                UserDB.user_mail,
                UserDB.user_desc,
                UserDB.user_avatar,
                UserDB.sd_id,
                UserDB.last_login,
                UserDB.dt_cr,
                UserDB.dt_up,
                UserDB.status,
            )
        )

        return await self.select_many(sql, **kwargs)

    async def delete(self, item_id: int) -> None:
        try:
            await super().delete(item_id)
        except IdNotFoundException:
            raise UserIdNotFound(item_id)

    async def update_last_login(self, item_id: int) -> None:
        sql = (
            update(UserDB)
            .where(UserDB.id == item_id)
            .values(last_login=datetime.now())
            .returning(UserDB.id)
        )
        async with self.session_maker.begin() as session:
            item = await session.scalar(sql)
            if not item:
                raise UserIdNotFound(item_id)
            await session.flush()

    @staticmethod
    def _parse_error(err: DBAPIError, model: UserModel) -> None:
        match err.orig.__cause__.constraint_name:  # type: ignore
            case 'users_pk':
                raise UserIdAlreadyExists(model.id) from err
            case 'users_uq_user_name':
                raise UserNameAlreadyExists(model.user_name) from err
            case 'users_uq_user_mail':
                raise UserMailAlreadyExists(model.user_mail) from err  # type: ignore
            case _:
                logger.error('Unknown error occurred', extra={'error': repr(err)})
                raise err
