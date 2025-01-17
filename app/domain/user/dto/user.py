from datetime import datetime
from typing import TypeAlias

from pydantic import EmailStr

from app.domain.common.dto.base import (
    DtCrUpModelMixin,
    DTO,
    IDModelMixin,
    LastLoginMixin,
    StatusModelMixin,
)
from app.domain.common.dto.helper import IdField, StatusField
from app.domain.common.dto.pagination import PaginatedItemsDTO
from app.domain.user.dto.helper import (
    SubdivisionIdOptionalField,
    UserAvatarOptionalField,
    UserDescOptionalField,
    UserMailOptionalField,
    UserNameField,
    UserPassField,
    VerificationCodeOptionalField,
)


class BaseUser(DTO):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_desc: str | None = UserDescOptionalField
    user_avatar: str | None = UserAvatarOptionalField
    sd_id: int | None = SubdivisionIdOptionalField


class UserDto(StatusModelMixin, DtCrUpModelMixin, LastLoginMixin, BaseUser, IDModelMixin):
    ...


class UserFullDto(StatusModelMixin, DtCrUpModelMixin, LastLoginMixin, BaseUser, IDModelMixin):
    ...


class UserCredentialCodes(DTO):
    user_id: int
    codes: list[str]


class UserDataDto(StatusModelMixin, BaseUser):
    ...


class UserCreateDto(UserDataDto):
    user_pass: str = UserPassField


class UserUpdateDto(DTO, IDModelMixin):
    update_data: UserDataDto


class UserAuthDto(DTO):
    id: int = IdField
    user_name: str = UserNameField
    user_pass: str = UserPassField
    user_mail: EmailStr | None = UserMailOptionalField
    status: bool = StatusField


class UserVerifyDto(DTO):
    id: int = IdField
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    sd_id: int | None = SubdivisionIdOptionalField
    verification_code: str | None = VerificationCodeOptionalField
    dt_ac: datetime | None
    status: bool = StatusField


class _UserResetPasswordDto(DTO):
    id: int = IdField
    verification_code: str | None = VerificationCodeOptionalField
    dt_ac: datetime | None
    status: bool = StatusField


class UserSignupDto(DTO):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_pass: str = UserPassField
    sd_id: int | None = SubdivisionIdOptionalField


UsersDto: TypeAlias = PaginatedItemsDTO[UserDto]
