from app.domain.common.exceptions import ConflictException, IdNotFoundException
from app.domain.common.exceptions.base import NotFoundException


class UserIdNotFound(IdNotFoundException):
    def __init__(self, item_id: int):
        super().__init__(item_id, 'User with id=<{}> not found')


class UserIdAlreadyExists(ConflictException):
    def __init__(self, item_id: int):
        super().__init__(f'User with id=<{item_id}> already exists')


class UserNameNotFound(NotFoundException):
    def __init__(self, user_name: str):
        super().__init__(f'User with name=<{user_name}> not found')


class UserNameAlreadyExists(ConflictException):
    def __init__(self, user_name: str):
        super().__init__(f'User with name=<{user_name}> already exists')


class UserMailNotFound(NotFoundException):
    def __init__(self, user_email: str):
        super().__init__(f'User with email=<{user_email}> not found')


class UserMailAlreadyExists(ConflictException):
    def __init__(self, user_mail: str):
        super().__init__(f'User with e-mail=<{user_mail}> already exists')
