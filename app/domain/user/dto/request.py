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


class UserSignInRequest(BaseModel):
    username: str = UserNameField
    password: str = UserPassField


class UserSignUpRequest(BaseModel):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_pass: str = UserPassField
    sd_id: int | None = SubdivisionIdOptionalField

# class PasswordUpdateRequest(BaseModel):
#     user_pass: str = helper.UserPassNewField


# class PasswordChangeRequest(BaseModel):
#     password_old: str = helper.UserPassOldField
#     password_new: str = helper.UserPassNewField
