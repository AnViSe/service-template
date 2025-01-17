from contextlib import asynccontextmanager, AsyncExitStack
from typing import AsyncIterator

from app.core.config import Config
from app.infrastructure.database.adapters.postgres import PostgresDB


class Adapters:
    def __init__(
        self,
        postgres: PostgresDB,
    ):
        self.postgres = postgres

    @classmethod
    @asynccontextmanager
    async def create(cls, config: Config) -> AsyncIterator['Adapters']:
        async with AsyncExitStack() as stack:
            postgres = await stack.enter_async_context(PostgresDB(config.postgres.dsn, config.logging.echo_sql))

            yield cls(postgres)
