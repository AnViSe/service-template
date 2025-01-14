from pydantic import BaseModel

from app.domain.common.dto.helper import IdField, StatusField
from app.domain.user.dto.helper import EmailOptionalField, UserNameField, VerifyOptionalField
from app.domain.user.dto.user import UserFullDto


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class SignInInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    user: UserFullDto


class UserSignUpResponse(BaseModel):
    id: int = IdField
    username: str = UserNameField
    email: str | None = EmailOptionalField
    verify: str | None = VerifyOptionalField
    status: bool = StatusField

# class Permissions(BaseModel):
#     items: list[str]
