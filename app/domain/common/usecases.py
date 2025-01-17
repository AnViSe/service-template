from app.core.config import Config
from app.domain.permission.usecases import PermissionService
from app.domain.user.usecases import UserService
from app.infrastructure.database import Adapters
from app.utils.security import Security


class Services:
    def __init__(self, adapters: Adapters, config: Config):
        self.config = config
        self.adapters = adapters

        self.security = Security(config)

        self.user = UserService(self)
        self.permission = PermissionService(self)


__all__ = ['Services']
