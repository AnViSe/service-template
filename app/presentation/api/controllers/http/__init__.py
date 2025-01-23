from asyncpg.exceptions import PostgresError
from fastapi import APIRouter, FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.domain.common.exceptions import CustomException
from app.presentation.api.controllers.http import handlers
from .v1 import auth, permission, user, health


def setup_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, handlers.custom_exc_handler)  # type: ignore
    app.add_exception_handler(SQLAlchemyError, handlers.sql_exc_handler)  # type: ignore
    app.add_exception_handler(PostgresError, handlers.sql_exc_handler)  # type: ignore
    app.add_exception_handler(OSError, handlers.os_exc_handler)  # type: ignore
    app.add_exception_handler(Exception, handlers.default_exc_handler)


router_http = APIRouter()
router_http.include_router(health.router)
router_http.include_router(auth.router)
router_http.include_router(user.router)
