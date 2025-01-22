from datetime import datetime

from pydantic import EmailStr

from app.domain.common import dto as common_dto
from app.domain.user import dto as user_dto
from .fields import DtAcOptionalField, VerificationCodeOptionalField


class SignUpDto(common_dto.DTO):
    id: int = common_dto.IdField
    user_name: str = user_dto.UserNameField
    user_mail: str | None = user_dto.UserMailOptionalField
    verification_code: str | None = VerificationCodeOptionalField
    status: bool = common_dto.StatusField


# class _UserResetPasswordDto(common_dto.DTO):
#     id: int = common_dto.IdField
#     verification_code: str | None = VerificationCodeOptionalField
#     dt_ac: datetime | None = DtAcOptionalField
#     status: bool = common_dto.StatusField


class AuthDto(common_dto.DTO):
    id: int = common_dto.IdField
    user_name: str = user_dto.UserNameField
    user_pass: str = user_dto.UserPassField
    user_mail: EmailStr | None = user_dto.UserMailOptionalField
    sd_id: int | None = user_dto.SubdivisionIdOptionalField
    status: bool = common_dto.StatusField

class ResetDto(common_dto.DTO):
    id: int = common_dto.IdField
    verification_code: str | None = VerificationCodeOptionalField
    dt_ac: datetime | None = DtAcOptionalField
    status: bool = common_dto.StatusField


# class VerifyDto(common_dto.DTO):
#     id: int = common_dto.IdField
#     user_name: str = user_dto.UserNameField
#     user_mail: EmailStr | None = user_dto.UserMailOptionalField
#     sd_id: int | None = user_dto.SubdivisionIdOptionalField
#     verification_code: str | None = VerificationCodeOptionalField
#     dt_ac: datetime | None = DtAcOptionalField
#     status: bool = common_dto.StatusField

class VerifyDto(common_dto.DTO):
    id: int = common_dto.IdField
    user_name: str = user_dto.UserNameField
    user_desc: str | None = user_dto.UserDescOptionalField
    status: bool = common_dto.StatusField
