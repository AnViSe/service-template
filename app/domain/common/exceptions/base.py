class CustomException(Exception):
    def __init__(self, name: str, message: str, http_code: int = 500, internal_code: int = 0):
        super().__init__(message)
        self.error = name
        self.message = message
        self.http_code = http_code
        self.internal_code = internal_code


class RequestInvalidException(CustomException):
    def __init__(self, message: str = 'Request Invalid'):
        super().__init__('RequestInvalidException', message, http_code=400)


class UnauthorizedException(CustomException):
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__('UnauthorizedException', message, http_code=401)


class NotFoundException(CustomException):
    def __init__(self, message: str = 'Not Found'):
        super().__init__('NotFoundException', message, http_code=404)


class IdNotFoundException(CustomException):
    """Use message formatting

    If message is None returning: 'Item with id:<item_id> not found'
    Else: message.format(item_id)

    Example:
        IdNotFoundException(100, 'Object with id {} not found')

        Return message: 'Object with id 100 not found'

    :parameter item_id: int
    :parameter message: str | None
    """

    def __init__(self, item_id: int, message: str | None = None):
        super().__init__('IdNotFoundException', message, http_code=404)
        if message is None:
            self.message = f'Item with id:<{item_id}> not found'
        else:
            self.message = message.format(item_id)


class ConflictException(CustomException):
    def __init__(self, message: str = 'Conflict'):
        super().__init__('ConflictException', message, http_code=409)
