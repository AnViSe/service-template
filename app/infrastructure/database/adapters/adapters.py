import logging
from contextlib import asynccontextmanager, AsyncExitStack
from typing import AsyncIterator

from app.core.config import Config
from app.infrastructure.database.adapters.postgres import PostgresDB
from app.infrastructure.database.adapters.redis import RedisBus

logger = logging.getLogger('adapters')


class Adapters:
    def __init__(
        self,
        postgres: PostgresDB,
        bus: RedisBus,
    ):
        self.postgres = postgres
        self.bus = bus

    @classmethod
    @asynccontextmanager
    async def create(cls, config: Config) -> AsyncIterator['Adapters']:
        async with AsyncExitStack() as stack:
            postgres = await stack.enter_async_context(PostgresDB(config.postgres.dsn, config.logging.echo_sql))
            bus = await stack.enter_async_context(RedisBus(config.bus.dsn))

            yield cls(postgres, bus)
