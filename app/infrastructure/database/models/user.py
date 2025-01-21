from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import DateTime, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.user.model import UserModel
from app.infrastructure.database.models import DatabaseModel, int_pk_always_true, OwnerModel
from app.infrastructure.database.models.columns import datetime_ac, datetime_cr, datetime_up_no_update


class UserDB(DatabaseModel, OwnerModel):
    """Табличная модель Пользователь"""

    __tablename__ = 'users'
    __table_args__ = (
        Index('users_uq_user_name', text('lower(user_name)'), unique=True),
        Index('users_uq_user_mail', text('lower(user_mail)'), unique=True),
    )

    id: Mapped[int_pk_always_true]
    user_name: Mapped[str] = mapped_column(String(100), comment='Имя пользователя')
    user_mail: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='Адрес пользователя')
    user_pass: Mapped[str] = mapped_column(String(100), comment='Пароль пользователя')
    user_desc: Mapped[str | None] = mapped_column(String(150), nullable=True, comment='Описание пользователя')
    user_avatar: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='Аватар пользователя')
    sd_id: Mapped[int | None] = mapped_column(
        Integer, index=True, nullable=True, comment='Код подразделения пользователя'
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment='Последний вход')
    verification_code: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True, comment='Проверочный код'
    )

    # roles: Mapped[list['RoleDB']] = relationship(
    #     'RoleDB', secondary=users_roles, back_populates='users', order_by='RoleDB.role_code'
    # )
    # permissions: Mapped[list['PermissionDB']] = relationship(
    #     'PermissionDB', secondary=users_perms, back_populates='users', order_by='PermissionDB.perm_code'
    # )

    dt_ac: Mapped[datetime_ac]
    dt_cr: Mapped[datetime_cr]
    dt_up: Mapped[datetime_up_no_update]

    def get_id(self) -> int | None:
        return self.id

    def to_domain_model(self) -> UserModel:
        return UserModel(
            id=self.id,
            user_name=self.user_name,
            sd_id=self.sd_id,
            user_mail=self.user_mail,
            user_pass=self.user_pass,
            user_desc=self.user_desc,
            user_avatar=self.user_avatar,
            # roles=[role.id for role in self.roles],
            # permissions=[permission.id for permission in self.permissions],
            dt_cr=self.dt_cr,
            dt_up=self.dt_up,
            status=self.status
        )

    @staticmethod
    def create_from_domain_model(model: UserModel) -> 'UserDB':
        item = UserDB(
            id=model.id,
            user_name=model.user_name,
            sd_id=model.sd_id,
            user_mail=model.user_mail,
            user_pass=model.user_pass,
            user_desc=model.user_desc,
            user_avatar=model.user_avatar,
            dt_cr=model.dt_cr,
            dt_up=model.dt_up,
            status=model.status
        )
        """
        Если пользователь создается с активным статусом, то дату активации проставляем автоматом
        """
        if model.status:
            item.dt_ac = datetime.now()
        else:
            if model.user_mail:
                item.verification_code = token_urlsafe(70)

        return item
