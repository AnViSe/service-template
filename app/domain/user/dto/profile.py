from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.domain.common.dto.base import DTO, IDModelMixin
from app.domain.user.dto.helper import (
    SubdivisionIdOptionalField,
    SubdivisionNameOptionalField, UserAvatarOptionalField,
    UserDescOptionalField,
    UserMailOptionalField,
    UserNameField,
)


class UserProfileDto(DTO, IDModelMixin):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_desc: str | None = UserDescOptionalField
    user_avatar: str | None = UserAvatarOptionalField
    sd_id: int | None = SubdivisionIdOptionalField
    sd_name: str | None = SubdivisionNameOptionalField
    last_login: datetime | None


class UserProfileDataDto(BaseModel):
    user_avatar: str | None = UserAvatarOptionalField


class UserProfileUpdateDto(DTO, IDModelMixin):
    update_data: UserProfileDataDto
