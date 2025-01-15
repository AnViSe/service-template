from abc import ABCMeta
from typing import Generic
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.models.base import AbstractDomainModel
from app.infrastructure.database.models.base import AbstractDatabaseModel


class BaseRepository(Generic[AbstractDatabaseModel], metaclass=ABCMeta):
    def __init__(self, model: type[AbstractDatabaseModel], session_maker: async_sessionmaker):
        self.model = model
        self.session_maker = session_maker

    async def create(self, model: AbstractDomainModel) -> AbstractDomainModel:
        async with self.session_maker() as session:
            model = self.model.create_from_domain_model(model)
            session.add(model)
            await session.flush()
            return model.to_domain_model()
