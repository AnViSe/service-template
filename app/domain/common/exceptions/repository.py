from app.domain.common.exceptions import CustomException


class RepositoryException(CustomException):
    def __init__(self, name: str = 'RepositoryException', message: str = 'Repository Exception'):
        super().__init__(name, message)


class ConnectEstablishingException(RepositoryException):
    def __init__(self, message: str = 'Connect Establishing Exception'):
        super().__init__('ConnectEstablishingException', message)


class UndefinedColumnException(RepositoryException):
    def __init__(self, message: str = 'Undefined Column Exception'):
        super().__init__('UndefinedColumnException', message)


class UndefinedTableException(RepositoryException):
    def __init__(self, message: str = 'Undefined Table Exception'):
        super().__init__('UndefinedTableException', message)


class ValidationException(RepositoryException):
    def __init__(self, message: str = 'Validation Exception'):
        super().__init__('ValidationException', message)


class ArgumentException(RepositoryException):
    def __init__(self, message: str = 'Argument Exception'):
        super().__init__('ArgumentException', message)


class AttributeException(RepositoryException):
    def __init__(self, message: str = 'Attribute Exception'):
        super().__init__('AttributeException', message)


class TypeException(RepositoryException):
    def __init__(self, message: str = 'Type Exception'):
        super().__init__('TypeException', message)
