from pydantic import BaseModel

from app.domain.common.dto.helper import StatusField
from app.domain.permission.dto import helper


class PermissionCreateRequest(BaseModel):
    perm_code: str = helper.PermCodeField
    perm_name: str = helper.PermNameField
    perm_desc: str | None = helper.PermDescOptionalField
    # users: list[int] | None
    # roles: list[int] | None
    status: bool = StatusField

