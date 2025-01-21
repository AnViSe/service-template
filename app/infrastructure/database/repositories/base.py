import logging
from abc import ABCMeta
from collections.abc import Sequence
from datetime import datetime
from typing import Generic, Type, TypeVar

import orjson
from sqlalchemy import (
    and_,
    Boolean,
    cast,
    ColumnElement, CTE,
    DateTime,
    delete,
    desc,
    Float,
    func,
    Integer,
    select,
    Select,
    String,
    text,
)
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.common.exceptions import IdNotFoundException
from app.domain.common.exceptions.base import NotFoundException
from app.domain.common.models.base import AbstractDomainModel
from app.infrastructure.database.models import AbstractDatabaseModel

SelectType = TypeVar('SelectType', Select, CTE)

logger = logging.getLogger('repository.base')


class BaseRepository(Generic[AbstractDatabaseModel], metaclass=ABCMeta):
    def __init__(
        self,
        model: Type[AbstractDatabaseModel],
        session_maker: async_sessionmaker,
    ):
        self.database_model = model
        self.session_maker = session_maker
        self.select_columns: dict = {}
        self.filter_fields: list[str] = []
        self.order_fields: list[str] = ['id']

    # def transaction(self, method):
    #     @wraps(method)
    #     async def wrapped(self, *args, **kwargs):
    #         async with self.session_maker() as session:
    #             try:
    #                 return await method(self, *args, session=session, **kwargs)
    #             except Exception as e:
    #                 await session.rollback()
    #                 raise e
    #             finally:
    #                 await session.close()
    #
    #     return wrapped

    async def create(self, model: AbstractDomainModel) -> AbstractDatabaseModel:
        async with self.session_maker.begin() as session:
            model = self.database_model.create_from_domain_model(model)
            session.add(model)
            await session.flush()
            return model

    async def create_get_id(self, model: AbstractDomainModel) -> int:
        db_item = self.database_model.create_from_domain_model(model)
        async with self.session_maker.begin() as session:
            session.add(db_item)
            try:
                await session.flush()
                await session.commit()
                return db_item.get_id()
            except IntegrityError as e:
                self._parse_error(e, model)

    async def update(self, item_id: int, model: AbstractDomainModel) -> None:
        sql = select(self.database_model).where(and_(self.database_model.id == item_id))
        async with self.session_maker.begin() as session:
            item = await session.scalar(sql)
            if not item:
                raise IdNotFoundException(item_id)
            item.update_from_domain_model(model)
            try:
                await session.flush()
            except IntegrityError as e:
                self._parse_error(e, model)

    async def retrieve_one(
        self,
        item_id: int | None = None,
        where_clause: list[ColumnElement[bool] | bool] | None = None,
    ) -> AbstractDatabaseModel | None:
        async with self.session_maker() as session:
            if item_id is not None:
                sql = select(self.database_model).where(and_(self.database_model.id == item_id))
                item = await session.scalar(sql)
                if not item:
                    raise IdNotFoundException(item_id)
                else:
                    return item
            if where_clause is not None:
                sql = select(self.database_model).where(and_(*where_clause))
                item = await session.scalar(sql)
                if not item:
                    raise NotFoundException
                else:
                    return item

    async def retrieve_all(self) -> Sequence[AbstractDatabaseModel]:
        sql = select(self.database_model)
        async with self.session_maker() as session:
            _exec = await session.scalars(sql)
            return _exec.all()

    async def delete(self, item_id: int) -> None:
        sql = delete(self.database_model).where(and_(self.database_model.id == item_id)).returning(
            self.database_model.id
        )
        async with self.session_maker.begin() as session:
            item = await session.scalar(sql)
            if not item:
                raise IdNotFoundException(item_id)
            else:
                await session.flush()

    def __gen_select_columns(self, sql: SelectType) -> None:
        for column in sql.column_descriptions:
            if column.get('entity', None) is not None:
                _table_name = column['entity'].__tablename__
            else:
                _table_name = 'cte'
            self.select_columns.setdefault(
                f'{_table_name}.{column["name"]}', f'{column["type"].python_type.__name__}'
            )

    def __gen_filter_columns(self, **kwargs):
        list_of_filters = []
        _f_l = []
        _f = kwargs.get('filters')
        if _f is not None:
            if isinstance(_f, str):
                _f = orjson.loads(_f)
            if isinstance(_f, list):
                _f_l.extend(_f)
            elif isinstance(_f, dict):
                _f_l.append(_f)

        if len(_f_l) > 0:
            for f in _f_l:
                _field = f.get('field')
                _match = f.get('match')
                _value = f.get('value')
                if _field is not None and _match is not None:
                    logger.debug(_field)
                    _column_type = self.select_columns.get(_field, None)
                    if _column_type is not None:
                        _value_type = type(_value).__name__
                        match _match:
                            case 'equals':
                                if _value is None:
                                    list_of_filters.append(cast(text(_field), String).is_(None))
                                else:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) == self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'str':
                                        list_of_filters.append(
                                            cast(text(_field), String) == self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'bool':
                                        list_of_filters.append(
                                            cast(text(_field), Boolean) == self.__get_value(_value, _column_type)
                                        )
                            case 'notEquals':
                                if _value is None:
                                    list_of_filters.append(cast(text(_field), String).is_not(None))
                                else:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) != self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'str':
                                        list_of_filters.append(
                                            cast(text(_field), String) != self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'bool':
                                        list_of_filters.append(
                                            cast(text(_field), Boolean) != self.__get_value(_value, _column_type)
                                        )
                            case 'startsWith':
                                if _value is not None:
                                    list_of_filters.append(
                                        cast(text(_field), String).istartswith(self.__get_value(_value, _column_type))
                                    )
                            case 'endsWith':
                                if _value is not None:
                                    list_of_filters.append(
                                        cast(text(_field), String).iendswith(self.__get_value(_value, _column_type))
                                    )
                            case 'contains':
                                if _value is not None:
                                    list_of_filters.append(
                                        cast(text(_field), String).icontains(self.__get_value(_value, _column_type))
                                    )
                            case 'notContains':
                                if _value is not None:
                                    list_of_filters.append(
                                        cast(text(_field), String).notilike(
                                            f'%{self.__get_value(_value, _column_type)}%'
                                        )
                                    )
                            case 'lt':
                                if _value is not None:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) < self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'float' and _column_type == _value_type:
                                        list_of_filters.append(
                                            cast(text(_field), Float) < self.__get_value(_value, _column_type)
                                        )
                            case 'lte':
                                if _value is not None:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) <= self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'float':
                                        list_of_filters.append(
                                            cast(text(_field), Float) <= self.__get_value(_value, _column_type)
                                        )
                            case 'gt':
                                if _value is not None:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) > self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'float':
                                        list_of_filters.append(
                                            cast(text(_field), Float) > self.__get_value(_value, _column_type)
                                        )
                            case 'gte':
                                if _value is not None:
                                    if _column_type == 'int':
                                        list_of_filters.append(
                                            cast(text(_field), Integer) >= self.__get_value(_value, _column_type)
                                        )
                                    if _column_type == 'float':
                                        list_of_filters.append(
                                            cast(text(_field), Float) >= self.__get_value(_value, _column_type)
                                        )
                            case 'dateIs':
                                if _value is not None and _column_type == 'datetime':
                                    list_of_filters.append(
                                        cast(text(_field), DateTime) == self.__get_value(_value, _column_type)
                                    )
                            case 'dateIsNot':
                                if _value is not None and _column_type == 'datetime':
                                    list_of_filters.append(
                                        cast(text(_field), DateTime) != self.__get_value(_value, _column_type)
                                    )
                            case 'dateBefore':
                                if _value is not None and _column_type == 'datetime':
                                    list_of_filters.append(
                                        cast(text(_field), DateTime) < self.__get_value(_value, _column_type)
                                    )
                            case 'dateAfter':
                                if _value is not None and _column_type == 'datetime':
                                    list_of_filters.append(
                                        cast(text(_field), DateTime) > self.__get_value(_value, _column_type)
                                    )
                            case _:
                                logger.warning(f'Неизвестное условие: {_match}')
                    else:
                        logger.warning(f'Поле: {_field} отсутствует в запросе.')
        return and_(*list_of_filters)

    def __gen_order_columns(self, **kwargs):
        _main_table_name: str | None = kwargs.get('main_table_name', None)
        if len(self.order_fields) > 0:
            _main_table_name = self.order_fields[0].split('.')[0]
        list_of_orders: list[str] = []
        if kwargs.get('sort') and isinstance(kwargs['sort'], str):
            list_of_orders.extend([str(f).lower().strip() for f in kwargs['sort'].split(',')])
        else:
            list_of_orders.extend(self.order_fields)
        _orders = []
        for field in list_of_orders:
            vector = '+'
            if field.startswith('-'):
                vector = '-'
                field = field[1:]
            if field.count('.') == 0:
                if _main_table_name is not None:
                    if self.select_columns.get(f'{_main_table_name}.{field}') is None:
                        field = f'cte.{field}'
                    else:
                        field = f'{_main_table_name}.{field}'
            if self.select_columns.get(field):
                _field = text(field)
                if vector == '-':
                    _orders.append(desc(_field))
                else:
                    _orders.append(_field)
            else:
                logger.warning(f'Поле: {field} отсутствует в запросе.')
        return _orders

    @staticmethod
    def __get_limits(**kwargs):
        if kwargs.get('page') and isinstance(kwargs['page'], int):
            page = kwargs.get('page')
            limit = kwargs.get('limit', 100)
            skip = page * limit - limit
        else:
            skip = kwargs.get('skip', 0)
            limit = kwargs.get('limit', 100)

        return skip, limit

    @staticmethod
    def __get_value(value: str, type_to: str | None, type_from: str | None = None):
        match type_to:
            case 'int':
                return int(value)
            case 'float':
                return float(value)
            case 'bool':
                match value:
                    case 'true':
                        return True
                    case '1':
                        return True
                    case _:
                        return False
            case 'datetime':
                return datetime.strptime(value, '%Y-%m-%d')
            case _:
                return value

    async def select_many(self, sql: SelectType, **kwargs):
        self.__gen_select_columns(sql)
        _skip, _limit = self.__get_limits(**kwargs)
        _sql = sql.where(self.__gen_filter_columns(**kwargs))
        _sql_count = select(func.count()).select_from(_sql.subquery())
        async with self.session_maker() as session:
            _record_count = await session.scalar(_sql_count)
            if _record_count > 0:
                _orders = self.__gen_order_columns(**kwargs)
                _exec = await session.execute(_sql.order_by(*_orders).limit(_limit).offset(_skip))
                return _skip, _record_count, _exec.mappings().all()
            else:
                return _skip, _record_count, []

    @staticmethod
    def _parse_error(err: DBAPIError, model: AbstractDomainModel) -> None:
        # logger.error('BaseRepository _parse_error', extra={'error': repr(err)})
        match err.orig.__cause__.constraint_name:  # type: ignore
            # case "pk_users":
            #     raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            # case "uq_users_username":
            #     raise UsernameAlreadyExistsError(str(user.username)) from err
            case _:
                raise err
