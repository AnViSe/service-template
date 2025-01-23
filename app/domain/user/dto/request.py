from pydantic import BaseModel, EmailStr

from app.domain.common import dto as common_dto
from .fields import (
    SubdivisionIdOptionalField,
    UserAvatarOptionalField,
    UserDescOptionalField,
    UserMailOptionalField,
    UserNameField,
    UserPassField,
)


class UserCreateRequest(BaseModel):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_pass: str = UserPassField
    sd_id: int | None = SubdivisionIdOptionalField
    user_avatar: str | None = UserAvatarOptionalField
    user_desc: str | None = UserDescOptionalField
    # roles: list[int] | None
    # permissions: list[int] | None
    status: bool = common_dto.StatusField
