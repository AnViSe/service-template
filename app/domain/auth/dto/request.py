from pydantic import BaseModel

from app.domain.user import dto as user_dto


class SignUpRequest(BaseModel):
    user_name: str = user_dto.UserNameField
    user_mail: str | None = user_dto.UserMailOptionalField
    user_pass: str = user_dto.UserPassField
    sd_id: int | None = user_dto.SubdivisionIdOptionalField


class PasswordChangeRequest(BaseModel):
    password_old: str = user_dto.UserPassOldField
    password_new: str = user_dto.UserPassNewField


class PasswordUpdateRequest(BaseModel):
    user_pass: str = user_dto.UserPassNewField
