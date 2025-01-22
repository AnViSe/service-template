from faststream import FastStream
from faststream.redis import RedisBroker

from app.core.config import Config
from app.presentation.api.controllers import bus


class FastStreamApp:
    def __init__(
            self,
            config: Config,
    ):
        self.broker = RedisBroker(config.bus.dsn.unicode_string())
        self.app = FastStream(self.broker)

    def initialize(self) -> 'FastStreamApp':
        # amqp.setup_middlewares(self.app)
        self.broker.include_router(bus.router)
        return self
