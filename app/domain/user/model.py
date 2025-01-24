from dataclasses import dataclass

from pydantic import EmailStr

from app.domain.common.models.aggregate import Aggregate


@dataclass
class UserModel(Aggregate):
    """Доменная модель Пользователь"""

    user_name: str
    user_mail: EmailStr | None
    user_pass: str
    user_desc: str | None
    user_avatar: str | None

    sd_id: int | None

    roles: list[int] | None
    permissions: list[int] | None

    @classmethod
    def create(
        cls,
        user_name: str,
        user_mail: EmailStr | None,
        sd_id: int | None,
        roles: list[int] | None,
        permissions: list[int] | None,
        user_desc: str | None = None,
        user_avatar: str | None = None,
        user_pass: str | None = None,
        status: bool = False,
    ) -> 'UserModel':
        user = UserModel(
            id=None,
            user_name=user_name,
            user_mail=user_mail,
            user_pass=user_pass,
            user_desc=user_desc,
            user_avatar=user_avatar,
            sd_id=sd_id,
            roles=roles if roles is not None else [],
            permissions=permissions if permissions is not None else [],
            dt_cr=None,
            dt_up=None,
            status=status,
        )
        return user
