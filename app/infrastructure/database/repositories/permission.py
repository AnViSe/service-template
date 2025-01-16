import logging

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import ConflictException, NotFoundException
from app.domain.permission.exceptions import NotFound, PermissionCodeAlreadyExists, PermissionIdAlreadyExists
from app.domain.permission.model import PermissionModel
from app.infrastructure.database.models.permission import PermissionDB
from app.infrastructure.database.repositories.base import BaseRepository

logger = logging.getLogger('repository.permission')


class PermissionRepository(BaseRepository[PermissionDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=PermissionDB, session_maker=session_maker)

    async def retrieve_many(self, **kwargs):
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

        return await self.select_data(sql, **kwargs)

    async def delete(self, item_id: int) -> None:
        try:
            await super().delete(item_id)
        except NotFoundException:
            raise NotFound(item_id=item_id)

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
