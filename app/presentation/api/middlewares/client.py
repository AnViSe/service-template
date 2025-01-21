from starlette.middleware.base import BaseHTTPMiddleware


class ClientMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.client = request.client.host
        response = await call_next(request)
        return response
