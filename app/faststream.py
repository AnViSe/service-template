import logging

from faststream import FastStream
from faststream.redis import RedisBroker

from app.core.config import Config
from app.presentation import api

logger = logging.getLogger('bus')


class FastStreamApp:
    def __init__(
        self,
        config: Config,
    ):
        self.broker = RedisBroker(config.bus.dsn.unicode_string(), logger=logger)
        self.app = FastStream(self.broker, logger=logger)

    def initialize(self) -> 'FastStreamApp':
        # amqp.setup_middlewares(self.app)
        self.broker.include_router(api.router_bus)
        return self
