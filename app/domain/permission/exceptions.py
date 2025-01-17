from app.domain.common.exceptions import ConflictException, IdNotFoundException


class PermissionIdNotFound(IdNotFoundException):
    def __init__(self, item_id: int):
        super().__init__(item_id, 'Permission with id=<{}> not found')


class PermissionIdAlreadyExists(ConflictException):
    def __init__(self, item_id: int):
        super().__init__(f'Permission with id=<{item_id}> already exists')


class PermissionCodeAlreadyExists(ConflictException):
    def __init__(self, perm_code: str):
        super().__init__(f'Permission with code=<{perm_code}> already exists')
