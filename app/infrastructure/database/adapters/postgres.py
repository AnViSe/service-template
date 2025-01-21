from typing import Self

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine

from app.infrastructure.database import repositories
from app.utils import Singleton


class PostgresDB(metaclass=Singleton):
    def __init__(
        self,
        pg_dsn: PostgresDsn,
        echo: bool = False,
        engine: AsyncEngine | None = None,
        session_maker: async_sessionmaker[AsyncSession] | None = None,
    ) -> None:
        self.__pg_dsn = pg_dsn
        self.__echo = echo
        self.__engine = engine
        self.__session_maker = session_maker

    async def __set_async_engine(self) -> None:
        if self.__engine is None:
            self.__engine = create_async_engine(
                self.__pg_dsn.unicode_string(),
                pool_pre_ping=True,
                echo=self.__echo,
            )

    async def __set_session_maker(self) -> None:
        if self.__session_maker is None:
            self.__session_maker = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.__engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    async def __set_repositories(self) -> None:
        if self.__session_maker is not None:
            self.user = repositories.UserRepository(self.__session_maker)
            self.permission = repositories.PermissionRepository(self.__session_maker)

    async def __aenter__(self) -> Self:
        await self.__set_async_engine()
        await self.__set_session_maker()
        await self.__set_repositories()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if self.__engine is not None:
            await self.__engine.dispose()
