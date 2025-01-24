import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from pydantic import ValidationError
from sqlalchemy.exc import ArgumentError, ProgrammingError

from app.domain.common import exceptions

logger = logging.getLogger('exception_mapper')

Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
# Func = Callable[Param, ReturnType]


def exception_mapper(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)

        # except IntegrityError as e:
        #     logger.error(e)
        #     if str(e.args[0]).find('UniqueViolationError') >= 0:
        #         raise repository.UniqueViolationException(e)
        #     if str(e.args[0]).find('NotNullViolationError') >= 0:
        #         raise repository.NotNullViolationException(e)
        #     if str(e.args[0]).find('ForeignKeyViolationError') >= 0:
        #         raise repository.ForeignKeyViolationException(e)
        #     if str(e.args[0]).find('CheckViolationError') >= 0:
        #         raise repository.CheckViolationException(e)
        #     raise repository.RepositoryException(e)
        except ArgumentError as e:
            logger.error('ArgumentError', extra={'error': repr(e)})
            raise exceptions.ArgumentException from e
        except ProgrammingError as e:
            logger.error('ProgrammingError', extra={'error': repr(e), 'statement': e.statement})
            orig = str(e.orig)
            msg = str(e.orig.__cause__).capitalize()
            if orig.find('UndefinedColumnError') >= 0:
                raise exceptions.UndefinedColumnException(msg) from e
            if orig.find('UndefinedTableError') >= 0:
                raise exceptions.UndefinedTableException(msg) from e
            raise exceptions.RepositoryException
        except ValidationError as e:
            logger.error('ValidationError', extra={'error': repr(e)})
            raise exceptions.ValidationException(str(e))
        except TimeoutError as e:
            logger.error('TimeoutError', extra={'error': repr(e)})
            raise exceptions.ConnectEstablishingException from e
        # except AttributeError as e:
        #     logger.error('AttributeError', extra={'error': repr(e)})
        #     raise exceptions.AttributeException(str(e))
        # except TypeError as e:
        #     logger.error('TypeError', extra={'error': repr(e)})
        #     raise exceptions.TypeException(str(e))

    return wrapped
