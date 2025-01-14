from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.common.dto.helper import (
    DtCrField,
    DtUpField,
    IdField,
    IdWithZeroField,
    ItemsOptionalField,
    # LastLoginOptionalField,
    # SDNameOptionalField,
    StatusField,
)


class DTO(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        extra='forbid',
        frozen=True,
        from_attributes=True
    )


class DtCrUpModelMixin(BaseModel):
    dt_cr: datetime = DtCrField
    dt_up: datetime | None = DtUpField


class StatusModelMixin(BaseModel):
    status: bool = StatusField


class IDModelMixin(BaseModel):
    id: int = IdField


class IDWithZeroModelMixin(BaseModel):
    id: int = IdWithZeroField


# class PermissionsIntMixin(BaseModel):
#     permissions: list[int] | None = ItemsOptionalField


# class RolesIntMixin(BaseModel):
#     roles: list[int] | None = ItemsOptionalField


# class UsersIntMixin(BaseModel):
#     users: list[int] | None = ItemsOptionalField


# class LastLoginMixin(BaseModel):
#     last_login: datetime | None = LastLoginOptionalField


# class SubdivisionMixin(BaseModel):
#     sd_name: str | None = SDNameOptionalField

