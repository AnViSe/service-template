from datetime import datetime
from typing import Annotated, Generic, TypeVar

from sqlalchemy import func, Identity, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, registry

from app.domain.common.models.base import AbstractDomainModel

convention = {
    'ix': '%(table_name)s_ix_%(column_0_name)s',
    'uq': '%(table_name)s_uq_%(column_0_name)s',
    'ck': '%(table_name)s_ck_%(constraint_name)s',
    'fk': '%(table_name)s_fk_%(column_0_name)s',
    'pk': '%(table_name)s_pk',
}

mapper_registry = registry(metadata=MetaData(naming_convention=convention))


def get_current_datetime():
    return datetime.now()


class Base(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata


int_pk_always_true = Annotated[int, mapped_column(Identity(always=True), primary_key=True, comment='Уникальный ключ')]
int_pk_always_false = Annotated[int, mapped_column(Identity(always=False), primary_key=True, comment='Уникальный ключ')]
int_pk_always_none = Annotated[int, mapped_column(primary_key=True, autoincrement=False, comment='Уникальный ключ')]
int_sort = Annotated[
    int, mapped_column(nullable=False, index=True, server_default='999', comment='Очередность отображения')]
datetime_ac = Annotated[datetime, mapped_column(nullable=True, comment='Активирована')]
datetime_cr = Annotated[datetime, mapped_column(server_default=func.now(), comment='Создана')]
datetime_up = Annotated[datetime | None, mapped_column(onupdate=get_current_datetime, comment='Изменена')]
datetime_up_no_update = Annotated[datetime | None, mapped_column(comment='Изменена')]
bool_status = Annotated[bool, mapped_column(index=True, server_default='true', comment='Статус')]


class DatabaseModel(Base):
    def to_domain_model(self) -> AbstractDomainModel:
        raise NotImplementedError()

    def create_from_domain_model(self, model: Generic[AbstractDomainModel]) -> 'DatabaseModel':
        raise NotImplementedError()


AbstractDatabaseModel = TypeVar('AbstractDatabaseModel', bound=DatabaseModel)
