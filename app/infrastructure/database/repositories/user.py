import logging

from sqlalchemy import and_, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.user.exceptions import UserIdAlreadyExists, UserIdNotFound, UserMailAlreadyExists, UserNameAlreadyExists
from app.domain.user.model import UserModel
from app.infrastructure.database.models.user import UserDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.user')


class UserRepository(BaseRepository[UserDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=UserDB, session_maker=session_maker)

    async def __update(self, item_id: int, model: UserModel) -> None:
        item = await self.retrieve_one(item_id)
        item.update_from_domain_model(model)
        async with self.session_maker.begin() as session:
            await session.flush()

    async def retrieve_one(self, item_id: int | None = None, ) -> UserDB | None:
        sql = select(self.database_model).where(and_(self.database_model.id == item_id))
        async with self.session_maker() as session:
            item = await session.scalar(sql)
            if not item:
                raise UserIdNotFound(item_id)
            else:
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
