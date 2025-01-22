from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration, faststream as faststream_integration

from app.core.config import Config, config
from app.core.ioc import AppProvider
from app.core.log.main import StructLogger
from app.fastapi import FastAPIApp
from app.faststream import FastStreamApp

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
    container = make_container()
    fastapi_app = FastAPIApp(config).initialize()
    fastapi_integration.setup_dishka(container, fastapi_app.app)
    return fastapi_app


def setup_faststream() -> FastStreamApp:
    container = make_container()
    faststream_app = FastStreamApp(config).initialize()
    faststream_integration.setup_dishka(container, faststream_app.app)
    return faststream_app
