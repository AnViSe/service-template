import logging

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.role import dto as role_dto
from app.domain.role.exceptions import (
    RoleCodeAlreadyExists,
    RoleIdAlreadyExists,
    RoleIdNotFound,
)
from app.domain.role.model import RoleModel
from app.infrastructure.database.models.role import RoleDB
from app.infrastructure.database.repositories import BaseRepository

logger = logging.getLogger('repository.role')


class RoleRepository(BaseRepository[RoleDB]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=RoleDB, session_maker=session_maker)

    async def get_full_by_id(self, item_id: int) -> role_dto.RoleFullDto:
        sql = (
            select(RoleDB)
            .where(RoleDB.id == item_id)
        )
        async with self.session_maker() as session:
            db_model = await session.scalar(sql)
            if not db_model:
                raise RoleIdNotFound(item_id)
            return role_dto.RoleFullDto.model_validate(db_model)

    async def get_many(self, **kwargs):
        self.order_fields = [f'{RoleDB.__tablename__}.id']

        sql = (
            select(
                RoleDB.id,
                RoleDB.role_code,
                RoleDB.role_name,
                RoleDB.role_desc,
                RoleDB.dt_cr,
                RoleDB.dt_up,
                RoleDB.status,
            )
        )

        return await self.select_many(sql, **kwargs)

    async def create_get_id(self, model: RoleModel, owner_id: int | None = None) -> int:
        db_model = RoleDB.create_from_domain_model(model)
        db_model.owner_cr = owner_id
        return await self.base_create_get_id(db_model)

    async def update(self, item_id: int, model: RoleModel, owner_id: int | None = None) -> None:
        sql_select = (
            select(RoleDB)
            .where(RoleDB.id == item_id)
        )
        async with self.session_maker.begin() as session:
            db_model = await session.scalar(sql_select)
            if not db_model:
                raise RoleIdNotFound(item_id)
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
            raise RoleIdNotFound(item_id)

    @staticmethod
    def _parse_error(err: DBAPIError, model: RoleModel) -> None:
        match err.orig.__cause__.constraint_name:  # type: ignore
            case 'roles_pk':
                raise RoleIdAlreadyExists(model.id) from err
            case 'roles_uq_role_code':
                raise RoleCodeAlreadyExists(model.role_code) from err
            case _:
                logger.error('Unknown error occurred', extra={'error': repr(err)})
                raise err
