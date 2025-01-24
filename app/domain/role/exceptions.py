from app.domain.common.exceptions import ConflictException, IdNotFoundException


class RoleIdNotFound(IdNotFoundException):
    def __init__(self, item_id: int):
        super().__init__(item_id, 'Role with id=<{}> not found')


class RoleIdAlreadyExists(ConflictException):
    def __init__(self, item_id: int):
        super().__init__(f'Role with id=<{item_id}> already exists')


class RoleCodeAlreadyExists(ConflictException):
    def __init__(self, perm_code: str):
        super().__init__(f'Role with code=<{perm_code}> already exists')
