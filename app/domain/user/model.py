from dataclasses import dataclass

from pydantic import EmailStr

from app.domain.common.models.aggregate import Aggregate


@dataclass
class UserModel(Aggregate):
    """Доменная модель Пользователь"""

    user_name: str
    sd_id: int | None
    user_mail: EmailStr | None
    user_pass: str
    user_desc: str | None
    user_avatar: str | None

    # roles: list[int] | None
    # permissions: list[int] | None

    @classmethod
    def create(
        cls,
        user_name: str,
        sd_id: int | None,
        user_mail: EmailStr | None,
        user_desc: str | None,
        user_avatar: str | None,
        # roles: list[int] | None,
        # permissions: list[int] | None,
        status: bool,
        user_pass: str | None = None,
    ) -> 'UserModel':
        user = UserModel(
            id=None,
            user_name=user_name,
            sd_id=sd_id,
            user_mail=user_mail,
            user_pass=user_pass,
            user_desc=user_desc,
            user_avatar=user_avatar,
            # roles=roles,
            # permissions=permissions,
            dt_cr=None,
            dt_up=None,
            status=status,
        )
        return user
