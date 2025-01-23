from app.core.config import Config
from app.infrastructure.database import Adapters
from app.infrastructure.usecases import AuthService, PermissionService, Security, UserService


class Services:
    def __init__(self, adapters: Adapters, config: Config):
        self.config = config
        self.adapters = adapters

        self.security = Security(config)

        self.auth = AuthService(self)

        self.user = UserService(self)
        self.permission = PermissionService(self)


__all__ = ['Services']
