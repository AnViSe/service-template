import logging
from typing import Any, Self

from faststream.redis import RedisBroker
from pydantic import RedisDsn

from app.utils import Singleton

logger = logging.getLogger('redis.bus')


class RedisBus(metaclass=Singleton):
    def __init__(
        self,
        redis_dsn: RedisDsn,
        faststream_broker: RedisBroker | None = None,
    ) -> None:
        self.__redis_dsn = redis_dsn
        self.__faststream_broker = faststream_broker
        self._connection = None

    async def publish(
        self,
        stream: str,
        message: Any,
    ) -> None:
        if self._connection is None:
            await self.__set_faststream_broker_connect()
        await self.__faststream_broker.publish(message=message, stream=stream)

    async def __set_faststream_broker(self) -> None:
        if self.__faststream_broker is None:
            self.__faststream_broker = RedisBroker(self.__redis_dsn.unicode_string())

    async def __set_faststream_broker_connect(self) -> None:
        if self.__faststream_broker and self._connection is None:
            self._connection = await self.__faststream_broker.connect()

    async def __aenter__(self) -> Self:
        await self.__set_faststream_broker()
        await self.__set_faststream_broker_connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
