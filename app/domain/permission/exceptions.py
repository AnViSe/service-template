from app.domain.common.exceptions import ConflictException, NotFoundException


class NotFound(NotFoundException):
    def __init__(self, item_id: int):
        super().__init__(f'Permission with id={item_id} not found')

class AlreadyExists(ConflictException):
    def __init__(self, perm_code: str):
        super().__init__(f'Permission with code={perm_code} already exists')
