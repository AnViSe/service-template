from app.core.config import Config
from app.domain.permission.usecases import PermissionService
from app.infrastructure.database import Adapters


class Services:
    def __init__(self, adapters: Adapters, config: Config):
        self.config = config
        self.adapters = adapters

        self.permission = PermissionService(self)


__all__ = ['Services']
