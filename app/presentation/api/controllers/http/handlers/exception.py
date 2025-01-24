import logging

from asyncpg import exceptions as apg_exc
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import exc as sa_exc

from app.domain.common.exceptions import CustomException
from ..v1.responses.base import BaseErrorResponse

logger = logging.getLogger('http.exception')


def custom_exc_handler(_: Request, exception: CustomException) -> JSONResponse:
    logger.error('Handle APP error', extra={'error': repr(exception)})
    return JSONResponse(
        status_code=exception.http_code,
        content=BaseErrorResponse(
            error=exception.error,
            message=exception.message,
        ).model_dump(exclude_none=True)
    )


def sql_exc_handler(_: Request, exception: sa_exc.SQLAlchemyError | apg_exc.PostgresError) -> JSONResponse:
    logger.error('Handle SQL error', extra={'error': repr(exception)})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseErrorResponse(
            error='SQLError',
            message=repr(exception.with_traceback(None)),
        ).model_dump(exclude_none=True)
    )


def os_exc_handler(_: Request, exception: OSError) -> JSONResponse:
    logger.error('Handle error', extra={'error': repr(exception)})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseErrorResponse(
            error='OSError',
            message=exception.strerror,
        ).model_dump(exclude_none=True)
    )


def default_exc_handler(_: Request, exception: Exception) -> JSONResponse:
    logger.error('Handle error', extra={'error': repr(exception)})
    logger.exception('Unknown exception occurred', extra={'error': repr(exception)})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseErrorResponse(
            error='UnknownError',
            message=repr(exception.with_traceback(None)),
        ).model_dump(exclude_none=True)
    )
