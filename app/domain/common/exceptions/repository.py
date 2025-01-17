from app.domain.common.exceptions import CustomException


class RepositoryException(CustomException):
    def __init__(self, message: str = 'Repository Exception'):
        super().__init__(message)


class ConnectEstablishingException(RepositoryException):
    def __init__(self, message: str = 'Connect Establishing Exception'):
        super().__init__(message)


class UndefinedColumnException(RepositoryException):
    def __init__(self, message: str = 'Undefined Column Exception'):
        super().__init__(message)


class UndefinedTableException(RepositoryException):
    def __init__(self, message: str = 'Undefined Table Exception'):
        super().__init__(message)


class ValidationException(RepositoryException):
    def __init__(self, message: str = 'Validation Exception'):
        super().__init__(message)


class ArgumentException(RepositoryException):
    def __init__(self, message: str = 'Argument Exception'):
        super().__init__(message)


class AttributeException(RepositoryException):
    def __init__(self, message: str = 'Attribute Exception'):
        super().__init__(message)


class TypeException(RepositoryException):
    def __init__(self, message: str = 'Type Exception'):
        super().__init__(message)
