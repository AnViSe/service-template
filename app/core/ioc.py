from dishka import from_context, Provider, Scope

from app.core.config import Config


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
