import logging

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.permission import dto as perm_dto
from app.domain.permission.exceptions import (
    PermissionCodeAlreadyExists,
    PermissionIdAlreadyExists,
    PermissionIdNotFound,
)
from app.domain.permission.model import PermissionModel
from app.infrastructure.database.models.permission import PermissionDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.permission')


class PermissionRepository(BaseRepository[PermissionDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=PermissionDB, session_maker=session_maker)

    async def get_full_by_id(self, item_id: int) -> perm_dto.PermissionFullDto:
        sql = (
            select(PermissionDB)
            .where(PermissionDB.id == item_id)
        )
        async with self.session_maker() as session:
            db_model = await session.scalar(sql)
            if not db_model:
                raise PermissionIdNotFound(item_id)
            return perm_dto.PermissionFullDto.model_validate(db_model)

    async def get_many(self, **kwargs):
        self.order_fields = [f'{PermissionDB.__tablename__}.id']

        sql = (
            select(
                PermissionDB.id,
                PermissionDB.perm_code,
                PermissionDB.perm_name,
                PermissionDB.perm_desc,
                PermissionDB.dt_cr,
                PermissionDB.dt_up,
                PermissionDB.status,
            )
        )

        return await self.select_many(sql, **kwargs)

    async def create_get_id(self, model: PermissionModel, owner_id: int | None = None) -> int:
        db_model = PermissionDB.create_from_domain_model(model)
        db_model.owner_cr = owner_id
        return await self.base_create_get_id(db_model)

    async def update(self, item_id: int, model: PermissionModel, owner_id: int | None = None) -> None:
        sql_select = (
            select(PermissionDB)
            .where(PermissionDB.id == item_id)
        )
        async with self.session_maker.begin() as session:
            db_model = await session.scalar(sql_select)
            if not db_model:
                raise PermissionIdNotFound(item_id)
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
            raise PermissionIdNotFound(item_id)

    @staticmethod
    def _parse_error(err: DBAPIError, model: PermissionModel) -> None:
        match err.orig.__cause__.constraint_name:  # type: ignore
            case 'permissions_pk':
                raise PermissionIdAlreadyExists(model.id) from err
            case 'permissions_uq_perm_code':
                raise PermissionCodeAlreadyExists(model.perm_code) from err
            case _:
                logger.error('Unknown error occurred', extra={'error': repr(err)})
                raise err
