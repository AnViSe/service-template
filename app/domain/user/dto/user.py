from typing import TypeAlias

from pydantic import EmailStr

from app.domain.circulars import ExtUser
from app.domain.common import dto as common_dto
from .fields import (
    SubdivisionIdOptionalField,
    UserAvatarOptionalField,
    UserDescOptionalField,
    UserMailOptionalField,
    UserNameField,
    UserPassField,
)
from .mixins import LastLoginMixin


class BaseUser(common_dto.DTO):
    user_name: str = UserNameField
    user_mail: EmailStr | None = UserMailOptionalField
    user_desc: str | None = UserDescOptionalField
    user_avatar: str | None = UserAvatarOptionalField
    sd_id: int | None = SubdivisionIdOptionalField


class UserDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    LastLoginMixin,
    BaseUser,
    common_dto.IDModelMixin,
):
    ...


class UserFullDto(
    common_dto.StatusModelMixin,
    common_dto.DtCrUpModelMixin,
    LastLoginMixin,
    ExtUser,
    BaseUser,
    common_dto.IDModelMixin,
):
    ...


class UserCredentialCodes(common_dto.DTO):
    user_id: int
    codes: list[str]


class UserDataDto(
    common_dto.StatusModelMixin,
    common_dto.PermissionsIntMixin,
    common_dto.RolesIntMixin,
    BaseUser,
):
    ...


class UserCreateDto(UserDataDto):
    user_pass: str = UserPassField


class UserUpdateDto(
    common_dto.DTO,
    common_dto.IDModelMixin,
):
    update_data: UserDataDto


UsersDto: TypeAlias = common_dto.PaginatedItemsDTO[UserDto]
