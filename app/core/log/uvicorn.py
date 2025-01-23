"""
This module contains the dictConfig based logging for uvicorn.
"""

from typing import Any

uvicorn_logging_config: dict[str, Any] = {
    "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                # "formatTime": "%Y-%m-%d %H:%M:%S.000",
                # "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                "format": "%(asctime)s [%(levelname)s] [uvicorn.e] %(message)s"
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                # "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                "format": "%(asctime)s [%(levelname)s] [uvicorn.a] %(message)s"
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                # "class": "logging.NullHandler"
                "class": "logging.StreamHandler"
            },
            "access": {
                "formatter": "access",
                # "class": "logging.NullHandler"
                "class": "logging.StreamHandler"
            }
        },
        "loggers": {
            "uvicorn.error": {
                "level": "INFO",
                "handlers": [
                    "default"
                ],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": [
                    "access"
                ],
                "propagate": False
            }
        }
}
