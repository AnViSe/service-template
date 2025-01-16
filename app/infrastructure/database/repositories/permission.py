from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import NotFoundException
from app.domain.permission.exceptions import AlreadyExists, NotFound
from app.domain.permission.model import PermissionModel
from app.infrastructure.database.models.permission import PermissionDB
from app.infrastructure.database.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[PermissionDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=PermissionDB, session_maker=session_maker)

    async def retrieve_many(self, **kwargs):
        self.order_fields = [f'{PermissionDB.__tablename__}.id']

        _sql = (
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

        return await self.select_data(_sql, **kwargs)

    async def delete(self, item_id: int) -> None:
        try:
            await super().delete(item_id)
        except NotFoundException:
            raise NotFound(item_id=item_id)

    @staticmethod
    def _parse_error(err: DBAPIError, model: PermissionModel) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            # case "pk_users":
            #     raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case "permissions_uq_perm_code":
                raise AlreadyExists(str(model.perm_code)) from err
            case _:
                super()._parse_error(err, model)
