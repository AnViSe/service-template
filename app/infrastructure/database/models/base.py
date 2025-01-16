from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, registry

convention = {
    'ix': '%(table_name)s_ix_%(column_0_name)s',
    'uq': '%(table_name)s_uq_%(column_0_name)s',
    'ck': '%(table_name)s_ck_%(constraint_name)s',
    'fk': '%(table_name)s_fk_%(column_0_name)s',
    'pk': '%(table_name)s_pk',
}

mapper_registry = registry(metadata=MetaData(naming_convention=convention))


class Base(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata
