from datetime import datetime
from typing import Annotated

from sqlalchemy import func, Identity
from sqlalchemy.orm import mapped_column

def get_current_datetime():
    return datetime.now()

int_pk_always_true = Annotated[int, mapped_column(Identity(always=True), primary_key=True, comment='Уникальный ключ')]
int_pk_always_false = Annotated[int, mapped_column(Identity(always=False), primary_key=True, comment='Уникальный ключ')]
int_pk_always_none = Annotated[int, mapped_column(primary_key=True, autoincrement=False, comment='Уникальный ключ')]
int_sort = Annotated[
    int, mapped_column(nullable=False, index=True, server_default='999', comment='Очередность отображения')]
datetime_ac = Annotated[datetime, mapped_column(nullable=True, comment='Активирована')]
datetime_cr = Annotated[datetime, mapped_column(server_default=func.now(), comment='Создана')]
datetime_up = Annotated[datetime | None, mapped_column(nullable=True, onupdate=get_current_datetime, comment='Изменена')]
datetime_up_no_update = Annotated[datetime | None, mapped_column(comment='Изменена')]
bool_status = Annotated[bool, mapped_column(index=True, server_default='true', comment='Статус')]
