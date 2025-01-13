from dishka import AsyncContainer, make_async_container

from app.core.config import Config
from app.core.ioc import AppProvider

config = Config()


def make_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        context={
            Config: config,
        }
    )
