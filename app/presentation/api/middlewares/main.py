from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .context import RequestIdMiddleware
from .ratelimiting import RateLimitMiddleware
from .structlog import StructLogMiddleware


def setup_middlewares(app: FastAPI) -> None:
    """Middlewares work from down to up"""

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=600,
    )
    app.add_middleware(
        TrustedHostMiddleware,  # type: ignore
        allowed_hosts=['*'],
    )
    app.add_middleware(RateLimitMiddleware)  # type: ignore
    app.add_middleware(StructLogMiddleware)  # type: ignore
    app.add_middleware(RequestIdMiddleware)  # type: ignore
