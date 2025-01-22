from datetime import datetime

from pydantic import BaseModel

from .fields import DtCrField, DtUpOptionalField, IdField, StatusField


class DtCrUpModelMixin(BaseModel):
    dt_cr: datetime = DtCrField
    dt_up: datetime | None = DtUpOptionalField


class StatusModelMixin(BaseModel):
    status: bool = StatusField


class IDModelMixin(BaseModel):
    id: int = IdField

# class IDWithZeroModelMixin(BaseModel):
#     id: int = IdWithZeroField


# class PermissionsIntMixin(BaseModel):
#     permissions: list[int] | None = ItemsOptionalField


# class RolesIntMixin(BaseModel):
#     roles: list[int] | None = ItemsOptionalField


# class UsersIntMixin(BaseModel):
#     users: list[int] | None = ItemsOptionalField


# class SubdivisionMixin(BaseModel):
#     sd_name: str | None = SDNameOptionalField
