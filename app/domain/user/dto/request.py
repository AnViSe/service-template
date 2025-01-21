from pydantic import BaseModel, EmailStr

from app.domain.common.dto.helper import StatusField
from app.domain.user.dto import helper


class UserCreateRequest(BaseModel):
    user_name: str = helper.UserNameField
    user_mail: EmailStr | None = helper.UserMailOptionalField
    user_pass: str = helper.UserPassField
    sd_id: int | None = helper.SubdivisionIdOptionalField
    user_avatar: str | None = helper.UserAvatarOptionalField
    user_desc: str | None = helper.UserDescOptionalField
    # roles: list[int] | None
    # permissions: list[int] | None
    status: bool = StatusField


class UserSignInRequest(BaseModel):
    username: str = helper.UserNameField
    password: str = helper.UserPassField

class UserSignUpRequest(BaseModel):
    user_name: str = helper.UserNameField
    user_mail: EmailStr | None = helper.UserMailOptionalField
    user_pass: str = helper.UserPassField
    sd_id: int | None = helper.SubdivisionIdOptionalField


# class PasswordUpdateRequest(BaseModel):
#     user_pass: str = helper.UserPassNewField


# class PasswordChangeRequest(BaseModel):
#     password_old: str = helper.UserPassOldField
#     password_new: str = helper.UserPassNewField
