from starlette.middleware.base import BaseHTTPMiddleware
from uuid6 import uuid7


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.request_id = uuid7()
        response = await call_next(request)
        return response
