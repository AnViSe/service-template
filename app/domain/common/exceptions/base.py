class CustomException(Exception):
    def __init__(self, message: str, internal_code: int = 0, http_code: int = 500):
        super().__init__(message)
        self.internal_code = internal_code
        self.http_code = http_code
        self.message = message


class RequestInvalid(CustomException):
    def __init__(self, message: str = 'Request Invalid'):
        super().__init__(message, internal_code=0, http_code=400)


class UnauthorizedException(CustomException):
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(message, internal_code=0, http_code=401)


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
        super().__init__(message, internal_code=0, http_code=404)
        if message is None:
            self.message = f'Item with id:<{item_id}> not found'
        else:
            self.message = message.format(item_id)


class ConflictException(CustomException):
    def __init__(self, message: str = 'Conflict'):
        super().__init__(message, internal_code=0, http_code=409)
