from app.domain.common.dto.base import DTO, IDModelMixin
from app.domain.common.dto.helper import StatusField
from app.domain.user.dto.helper import UserDescOptionalField, UserNameField


class ShortUser(DTO):
    user_name: str = UserNameField
    user_desc: str | None = UserDescOptionalField
    status: bool = StatusField


class UserShortDto(ShortUser, IDModelMixin):
    ...
