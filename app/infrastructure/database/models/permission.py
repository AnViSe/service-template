from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, bool_status, datetime_cr, datetime_up, int_pk_always_true


class PermissionDB(Base):
    """Табличная модель Разрешение"""

    __tablename__ = 'permissions'
    __table_args__ = (Index('permissions_uq_perm_code', text('lower(perm_code)'), unique=True),)

    id: Mapped[int_pk_always_true]
    perm_code = mapped_column(String(100), nullable=False, comment='Код разрешения')
    perm_name: Mapped[str] = mapped_column(String(150), nullable=False, comment='Имя разрешения')
    perm_desc = mapped_column(String(200), nullable=True, comment='Описание разрешения')

    dt_cr: Mapped[datetime_cr]
    dt_up: Mapped[datetime_up]
    status: Mapped[bool_status]
