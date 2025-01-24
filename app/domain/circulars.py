from app.domain.common.dto.base import DTO
from app.domain.common.dto.fields import StatusField
from app.domain.common.dto.mixins import IDModelMixin
from app.domain.permission.dto.fields import PermCodeField, PermNameField
from app.domain.role.dto.fields import RoleCodeField, RoleNameField
from app.domain.user.dto.fields import UserDescOptionalField, UserNameField


class ShortPermission(DTO):
    perm_code: str = PermCodeField
    perm_name: str = PermNameField
    status: bool = StatusField


class ShortRole(DTO):
    role_code: str = RoleCodeField
    role_name: str = RoleNameField
    status: bool = StatusField


class ShortUser(DTO):
    user_name: str = UserNameField
    user_desc: str | None = UserDescOptionalField
    status: bool = StatusField


class PermissionShortDto(ShortPermission, IDModelMixin):
    ...


class RoleShortDto(ShortRole, IDModelMixin):
    ...


class UserShortDto(ShortUser, IDModelMixin):
    ...


class ExtPermission(DTO):
    users: list[UserShortDto]
    roles: list[RoleShortDto]


class ExtRole(DTO):
    users: list[UserShortDto]
    permissions: list[PermissionShortDto]


class ExtUser(DTO):
    roles: list[RoleShortDto]
    permissions: list[PermissionShortDto]
