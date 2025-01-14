from dishka import AsyncContainer, make_async_container

from app.core.config import Config
from app.core.ioc import AppProvider
from app.core.log.main import StructLogger
from app.fastapi import FastAPIApp

config = Config()
logger = StructLogger(config)


def make_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        context={
            Config: config,
            StructLogger: logger,
        }
    )


def setup_fastapi() -> FastAPIApp:
    # container = make_container()
    fastapi_app = FastAPIApp(config).initialize()
    # fastapi_integration.setup_dishka(container, fastapi_app.app)
    return fastapi_app
