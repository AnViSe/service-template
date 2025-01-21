import structlog
from starlette.middleware.base import BaseHTTPMiddleware


class StructLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=str(request.state.request_id))
        structlog.contextvars.bind_contextvars(client_ip=str(request.client.host))
        response = await call_next(request)
        return response
