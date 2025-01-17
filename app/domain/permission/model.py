from dataclasses import dataclass

from app.domain.common.models.aggregate import Aggregate


@dataclass
class PermissionModel(Aggregate):
    """Доменная модель Разрешение"""

    perm_code: str
    perm_name: str
    perm_desc: str | None

    @classmethod
    def create(
        cls,
        perm_code: str,
        perm_name: str,
        perm_desc: str,
        status: bool,
    ) -> 'PermissionModel':
        model = PermissionModel(
            id=None,
            perm_code=perm_code,
            perm_name=perm_name,
            perm_desc=perm_desc,
            dt_cr=None,
            dt_up=None,
            status=status,
        )
        return model
