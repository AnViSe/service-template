from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.permission.model import PermissionModel
from app.infrastructure.database.models import (
    Base,
    bool_status,
    DatabaseModel,
    datetime_cr,
    datetime_up,
    int_pk_always_true,
)


class PermissionDB(DatabaseModel):
    """Табличная модель Разрешение"""

    __tablename__ = 'permissions'
    __table_args__ = (Index('permissions_uq_perm_code', text('lower(perm_code)'), unique=True),)

    id: Mapped[int_pk_always_true]
    perm_code: Mapped[str] = mapped_column(String(100), nullable=False, comment='Код разрешения')
    perm_name: Mapped[str] = mapped_column(String(150), nullable=False, comment='Имя разрешения')
    perm_desc: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='Описание разрешения')

    # dt_cr: Mapped[datetime_cr]
    # dt_up: Mapped[datetime_up]
    # status: Mapped[bool_status]

    def get_id(self) -> int | None:
        return self.id

    def to_domain_model(self) -> PermissionModel:
        return PermissionModel(
            id=self.id,
            perm_code=self.perm_code,
            perm_name=self.perm_name,
            perm_desc=self.perm_desc,
            dt_cr=self.dt_cr,
            dt_up=self.dt_up,
            status=self.status
        )

    @staticmethod
    def create_from_domain_model(model: PermissionModel) -> 'PermissionDB':
        return PermissionDB(
            id=model.id,
            perm_code=model.perm_code,
            perm_name=model.perm_name,
            perm_desc=model.perm_desc,
            dt_cr=model.dt_cr,
            dt_up=model.dt_up,
            status=model.status,
        )
