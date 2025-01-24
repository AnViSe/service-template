from dataclasses import dataclass

from app.domain.common.models.aggregate import Aggregate


@dataclass
class RoleModel(Aggregate):
    """Доменная модель Роль"""

    role_code: str
    role_name: str
    role_desc: str | None

    @classmethod
    def create(
        cls,
        role_code: str,
        role_name: str,
        role_desc: str,
        status: bool,
    ) -> 'RoleModel':
        model = RoleModel(
            id=None,
            role_code=role_code,
            role_name=role_name,
            role_desc=role_desc,
            dt_cr=None,
            dt_up=None,
            status=status,
        )
        return model
