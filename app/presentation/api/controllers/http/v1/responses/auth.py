from pydantic import BaseModel

from app.domain.common.dto.helper import IdField, StatusField
from app.domain.user.dto.helper import UserMailOptionalField, UserNameField, VerificationCodeOptionalField


class UserSignUpResponse(BaseModel):
    id: int = IdField
    user_name: str = UserNameField
    user_mail: str | None = UserMailOptionalField
    verification_code: str | None = VerificationCodeOptionalField
    status: bool = StatusField
