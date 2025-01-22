import logging
from typing import Any, Self

from faststream import FastStream
from faststream.redis import RedisBroker
from pydantic import RedisDsn

from app.utils import Singleton

logger = logging.getLogger('redis.bus')

class RedisBus(metaclass=Singleton):
    def __init__(
        self,
        redis_dsn: RedisDsn,
        faststream_broker: RedisBroker | None = None,
        faststream_app: FastStream | None = None,
    ) -> None:
        self.__redis_dsn = redis_dsn
        self.__faststream_broker = faststream_broker
        self.__faststream_app = faststream_app

    async def publish(
        self,
        message: Any,
        stream: str,
    ) -> None:
        if self.__faststream_broker is not None:
            await self.__faststream_broker.connect()
            await self.__faststream_broker.publish(message=message, stream=stream)
            logger.debug(f'To stream: {stream} publish message')
            logger.debug(message)

    async def __set_faststream_broker(self) -> None:
        if self.__faststream_broker is None:
            self.__faststream_broker = RedisBroker(self.__redis_dsn.unicode_string())

    async def __set_faststream_broker_connect(self) -> None:
        if self.__faststream_broker:
            await self.__faststream_broker.connect()

    async def __set_faststream_app(self) -> None:
        if self.__faststream_app is None:
            self.__faststream_app = FastStream(self.__faststream_broker)

    async def __aenter__(self) -> Self:
        await self.__set_faststream_broker()
        await self.__set_faststream_app()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
