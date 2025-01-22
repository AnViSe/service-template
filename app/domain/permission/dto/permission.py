from typing import TypeAlias

from pydantic import BaseModel

from app.domain.common import dto as common_dto
from .fields import PermCodeField, PermDescOptionalField, PermNameField


class BasePermission(common_dto.DTO):
    perm_code: str = PermCodeField
    perm_name: str = PermNameField
    perm_desc: str | None = PermDescOptionalField


class PermissionCreateRequest(BaseModel):
    perm_code: str = PermCodeField
    perm_name: str = PermNameField
    perm_desc: str | None = PermDescOptionalField
    # users: list[int] | None
    # roles: list[int] | None
    status: bool = common_dto.StatusField


class PermissionDataDto(
    common_dto.StatusModelMixin,
    BasePermission,
):
    ...


class PermissionUpdateDto(
    common_dto.DTO,
    common_dto.IDModelMixin,
):
    update_data: PermissionDataDto


class PermissionDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    BasePermission,
    common_dto.IDModelMixin,
):
    ...


class PermissionFullDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    BasePermission,
    common_dto.IDModelMixin,
):
    ...


PermissionsDto: TypeAlias = common_dto.PaginatedItemsDTO[PermissionDto]
