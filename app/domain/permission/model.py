from app.domain.common.models.base import DomainModel


class PermissionModel(DomainModel):
    """Доменная модель Разрешение"""

    perm_code: str
    perm_name: str
    perm_desc: str
