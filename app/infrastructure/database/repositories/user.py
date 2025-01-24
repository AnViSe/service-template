import logging

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.user import dto as user_dto
from app.domain.user.exceptions import (
    UserIdAlreadyExists,
    UserIdNotFound,
    UserMailAlreadyExists,
    UserNameAlreadyExists,
)
from app.domain.user.model import UserModel
from app.infrastructure.database.models.user import UserDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.user')


class UserRepository(BaseRepository[UserDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=UserDB, session_maker=session_maker)

    # async def get_by_id(self, item_id: int) -> user_dto.UserDto:
    #     try:
    #         db_model = await self.base_get_one(item_id=item_id)
    #         return user_dto.UserDto.model_validate(db_model)
    #     except IdNotFoundException as e:
    #         raise UserIdNotFound(item_id) from e

    async def get_full_by_id(self, item_id: int) -> user_dto.UserFullDto:
        sql = (
            select(UserDB)
            # .options(subqueryload(UserDB.roles))
            # .options(subqueryload(UserDB.permissions))
            .where(UserDB.id == item_id)
        )
        async with self.session_maker() as session:
            db_model = await session.scalar(sql)
            if not db_model:
                raise UserIdNotFound(item_id)
            return user_dto.UserFullDto.model_validate(db_model)

    async def get_many(self, **kwargs):
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

    async def create_get_id(self, model: UserModel, owner_id: int | None = None) -> int:
        db_model = UserDB.create_from_domain_model(model)
        db_model.owner_cr = owner_id
        return await self.base_create_get_id(db_model)

    async def update(self, item_id: int, model: UserModel, owner_id: int | None = None) -> None:
        sql_select = (
            select(UserDB)
            .where(UserDB.id == item_id)
        )
        async with self.session_maker.begin() as session:
            db_model = await session.scalar(sql_select)
            if not db_model:
                raise UserIdNotFound(item_id)
            db_model.update_from_domain_model(model)
            db_model.owner_up = owner_id
            try:
                await session.flush()
                await session.commit()
            except IntegrityError as e:
                self._parse_error(e, model)

    async def delete(self, item_id: int, owner_id: int | None = None) -> None:
        try:
            await self.base_delete(item_id)
        except IdNotFoundException:
            raise UserIdNotFound(item_id)

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
