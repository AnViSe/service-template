from app.domain.common.exceptions import RequestInvalid, UnauthorizedException
from app.domain.common.exceptions.base import NotFoundException


class UserNotActive(UnauthorizedException):
    def __init__(self, user_name: str):
        super().__init__(f'User with name=<{user_name}> is not active')


class UserMailNotVerified(RequestInvalid):
    def __init__(self, user_mail: str):
        super().__init__(f'User with email=<{user_mail}> is not verified')

class PasswordWrong(UnauthorizedException):
    def __init__(self):
        super().__init__('Password is wrong')


class VerificationCodeNotFound(NotFoundException):
    def __init__(self):
        super().__init__('Verification code not found')


class TokenInvalid(UnauthorizedException):
    def __init__(self):
        super().__init__("Can't decode token.")


class TokenPayload(UnauthorizedException):
    def __init__(self):
        super().__init__('Token payload is invalid.')


class TokenPayloadUser(UnauthorizedException):
    def __init__(self):
        super().__init__('Token payload does not consist user.')


class TokenPayloadUserId(UnauthorizedException):
    def __init__(self):
        super().__init__('Token payload does not consist user.id')


class TokenExpired(UnauthorizedException):
    def __init__(self):
        super().__init__('Token expired.')
