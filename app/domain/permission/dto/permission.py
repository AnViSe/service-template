from typing import TypeAlias

from app.domain.common.dto.base import (
    DtCrUpModelMixin,
    DTO,
    IDModelMixin,
    StatusModelMixin,
)
from app.domain.common.dto.pagination import PaginatedItemsDTO
from app.domain.permission.dto.helper import PermCodeField, PermDescOptionalField, PermNameField


class BasePermission(DTO):
    perm_code: str = PermCodeField
    perm_name: str = PermNameField
    perm_desc: str | None = PermDescOptionalField


class PermissionDataDto(StatusModelMixin, BasePermission):
    ...


class PermissionUpdateDto(DTO, IDModelMixin):
    update_data: PermissionDataDto


class PermissionDto(StatusModelMixin, DtCrUpModelMixin, BasePermission, IDModelMixin):
    ...


class PermissionFullDto(StatusModelMixin, DtCrUpModelMixin, BasePermission, IDModelMixin):
    ...


PermissionsDto: TypeAlias = PaginatedItemsDTO[PermissionDto]
