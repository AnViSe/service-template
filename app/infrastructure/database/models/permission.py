from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.permission.model import PermissionModel
from app.infrastructure.database.models import DatabaseModel, DtCrUpModel, int_pk_always_true, OwnerModel
from app.infrastructure.database.models.relations import users_perms


class PermissionDB(OwnerModel, DtCrUpModel, DatabaseModel):
    """Табличная модель Разрешение"""

    __tablename__ = 'permissions'
    __table_args__ = (Index('permissions_uq_perm_code', text('lower(perm_code)'), unique=True),)

    id: Mapped[int_pk_always_true]
    perm_code: Mapped[str] = mapped_column(String(100), nullable=False, comment='Код разрешения')
    perm_name: Mapped[str] = mapped_column(String(150), nullable=False, comment='Имя разрешения')
    perm_desc: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='Описание разрешения')

    # roles: Mapped[list['RoleDB']] = relationship(
    #     'RoleDB', secondary=roles_perms, back_populates='permissions', order_by='RoleDB.role_code'
    # )
    users: Mapped[list['UserDB']] = relationship(
        'UserDB', secondary=users_perms, back_populates='permissions', order_by='UserDB.user_name'
    )

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
