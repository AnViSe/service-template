import logging
import os
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog
from sqlalchemy import log as sa_log

from .processors import get_render_processor, sqlalchemy_processor
from ..config import Config, LoggingConfig


def config_logger(cfg: LoggingConfig, dev_mode: bool = False) -> None:
    # Mute SQLAlchemy default logger handler
    sa_log._add_default_handler = lambda _: None

    common_processors: list[structlog.types.Processor] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt='%Y-%m-%d %H:%M:%S.%f', utc=False),
        structlog.contextvars.merge_contextvars,
        structlog.processors.dict_tracebacks,  # Трассировка стека при ошибке
        # structlog.processors.CallsiteParameterAdder(
        #     (
        #         structlog.processors.CallsiteParameter.FUNC_NAME,
        #         structlog.processors.CallsiteParameter.LINENO,
        #     )
        # ),
    ]

    structlog_processors: list[structlog.types.Processor] = [
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    logging_processors = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        sqlalchemy_processor,
    ]

    handlers: list[logging.Handler] = []

    if dev_mode:
        logging_console_processors = [
            *logging_processors,
            get_render_processor(render_json_logs=False, colors=True),
        ]
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=common_processors,
            processors=logging_console_processors,
        )
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)
    else:
        logging_file_processors = [
            *logging_processors,
            get_render_processor(render_json_logs=cfg.json_format, colors=False),
        ]
        if cfg.file_path:
            cfg.file_path.parent.mkdir(parents=True, exist_ok=True)
            log_path = Path.joinpath(cfg.file_path, cfg.file_name)

            if os.name == 'nt':
                file_handler = logging.FileHandler(
                    filename=str(log_path),
                    encoding='utf-8',
                )
            else:
                file_handler = RotatingFileHandler(
                    filename=str(log_path),
                    encoding='utf-8',
                    maxBytes=1024 * 1024 * cfg.file_size,
                    backupCount=cfg.file_count,
                )

            file_handler.set_name('file')
            file_handler.setLevel(cfg.level)
            file_formatter = structlog.stdlib.ProcessorFormatter(
                foreign_pre_chain=common_processors,
                processors=logging_file_processors,
            )
            file_handler.setFormatter(file_formatter)
            handlers.append(file_handler)

    logging.basicConfig(
        handlers=handlers,
        level=cfg.level,
    )

    structlog.configure(
        processors=[
            *common_processors,
            *structlog_processors,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


class StructLogger:
    def __init__(self, cfg: Config):
        config_logger(cfg.logging, cfg.app.debug)
        self.logger = structlog.get_logger(cfg.logging.logger_name)

    @staticmethod
    def _to_snake_case(name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    def bind(self, *args, **new_values):
        for arg in args:
            # if not issubclass(type(arg), Base):
            #     self.logger.error(
            #         "Unsupported argument when trying to log."
            #         f"Unnamed argument must be a subclass of Base. Invalid argument: {type(arg).__name__}"
            #     )
            #     continue

            key = self._to_snake_case(type(arg).__name__)

            structlog.contextvars.bind_contextvars(**{key: arg.id})

        structlog.contextvars.bind_contextvars(**new_values)

    @staticmethod
    def unbind(*keys: str):
        structlog.contextvars.unbind_contextvars(*keys)

    def debug(self, event: str | None = None, *args, **kwargs):
        self.logger.debug(event, *args, **kwargs)

    def info(self, event: str | None = None, *args, **kwargs):
        self.logger.info(event, *args, **kwargs)

    def warning(self, event: str | None = None, *args, **kwargs):
        self.logger.warning(event, *args, **kwargs)

    warn = warning

    def error(self, event: str | None = None, *args, **kwargs):
        self.logger.error(event, *args, **kwargs)

    def critical(self, event: str | None = None, *args, **kwargs):
        self.logger.critical(event, *args, **kwargs)

    def exception(self, event: str | None = None, *args, **kwargs):
        self.logger.exception(event, *args, **kwargs)
