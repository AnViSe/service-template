from dishka import from_context, provide, Provider, Scope

from app.domain.common.usecases import Services
from .config import Config
from ..infrastructure.database import Adapters


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_adapters(self, config: Config) -> Adapters:
        async with Adapters.create(config) as adapters:
            return adapters

    services = provide(Services, scope=Scope.REQUEST)
