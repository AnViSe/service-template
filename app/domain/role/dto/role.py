from typing import TypeAlias

from pydantic import BaseModel

from app.domain.common import dto as common_dto
from .fields import RoleCodeField, RoleDescOptionalField, RoleNameField


class BaseRole(common_dto.DTO):
    role_code: str = RoleCodeField
    role_name: str = RoleNameField
    role_desc: str | None = RoleDescOptionalField


class RoleCreateRequest(BaseModel):
    role_code: str = RoleCodeField
    role_name: str = RoleNameField
    role_desc: str | None = RoleDescOptionalField
    # users: list[int] | None
    # roles: list[int] | None
    status: bool = common_dto.StatusField


class RoleDataDto(
    common_dto.StatusModelMixin,
    BaseRole,
):
    ...


class RoleUpdateDto(
    common_dto.DTO,
    common_dto.IDModelMixin,
):
    update_data: RoleDataDto


class RoleDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    BaseRole,
    common_dto.IDModelMixin,
):
    ...


class RoleFullDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    BaseRole,
    common_dto.IDModelMixin,
):
    ...


RolesDto: TypeAlias = common_dto.PaginatedItemsDTO[RoleDto]
