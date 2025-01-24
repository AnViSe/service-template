from sqlalchemy import Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.role.model import RoleModel
from app.infrastructure.database.models import DatabaseModel, DtCrUpModel, int_pk_always_true, OwnerModel


class RoleDB(OwnerModel, DtCrUpModel, DatabaseModel):
    """Табличная модель Роль"""

    __tablename__ = 'roles'
    __table_args__ = (Index('roles_uq_role_code', text('lower(role_code)'), unique=True),)

    id: Mapped[int_pk_always_true]
    role_code: Mapped[str] = mapped_column(String(100), nullable=False, comment='Код роли')
    role_name: Mapped[str] = mapped_column(String(150), nullable=False, comment='Имя роли')
    role_desc: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='Описание роли')

    def get_id(self) -> int | None:
        return self.id

    def to_domain_model(self) -> RoleModel:
        return RoleModel(
            id=self.id,
            role_code=self.role_code,
            role_name=self.role_name,
            role_desc=self.role_desc,
            dt_cr=self.dt_cr,
            dt_up=self.dt_up,
            status=self.status
        )

    @staticmethod
    def create_from_domain_model(model: RoleModel) -> 'RoleDB':
        return RoleDB(
            id=model.id,
            role_code=model.role_code,
            role_name=model.role_name,
            role_desc=model.role_desc,
            dt_cr=model.dt_cr,
            dt_up=model.dt_up,
            status=model.status,
        )
