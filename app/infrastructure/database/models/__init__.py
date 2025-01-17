from typing import Generic, TypeVar

from sqlalchemy.orm import Mapped

from app.domain.common.models.base import AbstractDomainModel
from .base import Base
from .columns import bool_status, datetime_cr, datetime_up, int_pk_always_true, owner_cr, owner_up


class OwnerModel:
    __abstract__ = True

    owner_cr: Mapped[owner_cr]
    owner_up: Mapped[owner_up]


class DatabaseModel(Base):

    __abstract__ = True

    dt_cr: Mapped[datetime_cr]
    dt_up: Mapped[datetime_up]
    status: Mapped[bool_status]

    def get_id(self) -> int | None:
        raise NotImplementedError

    def to_domain_model(self) -> AbstractDomainModel:
        raise NotImplementedError

    @staticmethod
    def create_from_domain_model(model: Generic[AbstractDomainModel]) -> 'DatabaseModel':
        raise NotImplementedError

    def update_from_domain_model(self, model: AbstractDomainModel):
        for key, value in model.to_dict({'id', 'user_pass'}).items():
            if not isinstance(value, list):
                setattr(self, key, value)


AbstractDatabaseModel = TypeVar('AbstractDatabaseModel', bound=DatabaseModel)

__all__ = [
    'AbstractDatabaseModel',
    'Base',
    'DatabaseModel',
    'OwnerModel',
    'bool_status',
    'datetime_cr',
    'datetime_up',
    'int_pk_always_true',
]
