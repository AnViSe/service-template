from app.core.config import Config
from app.infrastructure.database import Adapters
from app.infrastructure.usecases.auth import AuthService
from app.infrastructure.usecases.permission import PermissionService
from app.infrastructure.usecases.role import RoleService
from app.infrastructure.usecases.security import Security
from app.infrastructure.usecases.user import UserService


class Services:
    def __init__(self, adapters: Adapters, config: Config):
        self.config = config
        self.adapters = adapters

        self.security = Security(config)

        self.auth = AuthService(self)

        self.user = UserService(self)
        self.role = RoleService(self)
        self.permission = PermissionService(self)


__all__ = ['Services']
