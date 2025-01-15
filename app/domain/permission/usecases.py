from app.domain.common.usecases import Services
from app.domain.permission.dto.permission import PermissionDataDto, PermissionFullDto


class PermissionService:

    def __init__(self, service: 'Services'):
        self.service = service

    async def create_permission(self, item: PermissionDataDto) -> PermissionFullDto:
        return PermissionFullDto()
