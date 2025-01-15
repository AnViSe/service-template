import logging

from asyncpg import exceptions as apg_exc
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import exc as sa_exc

from app.domain.common.exceptions import CustomException

logger = logging.getLogger('http.exception')


def custom_exc_handler(_: Request, exception: CustomException) -> JSONResponse:
    # logger.error('Handle APP error', exc_info=exception, extra={'error': exception})
    logger.error('Handle APP error', extra={'error': exception.message})
    return JSONResponse(
        status_code=exception.http_code,
        content=dict(detail=exception.message),
    )


def sql_exc_handler(_: Request, exception: sa_exc.SQLAlchemyError | apg_exc.PostgresError) -> JSONResponse:
    logger.error('Handle SQL error', exc_info=exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(detail=repr(exception.with_traceback(None)))
    )


def exc_handler(_: Request, exception: Exception) -> JSONResponse:
    logger.error('Handle error', exc_info=exception, extra={'error': exception})
    logger.exception('Unknown exception occurred', exc_info=exception, extra={'error': exception})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(detail=repr(exception.with_traceback(None)))
    )
