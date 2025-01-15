from collections.abc import Callable
from typing import Any
from uuid import UUID

import orjson
import structlog

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]


def additionally_serialize(obj: object) -> Any:
    if isinstance(obj, UUID):
        return str(obj)
    # if isinstance(obj, aio_pika.Message):
    #     return obj.info()
    raise TypeError(f"TypeError: Type is not JSON serializable: {type(obj)}")


def serialize_to_json(data: Any, default: Any) -> str:
    return orjson.dumps(data, default=additionally_serialize).decode()


def get_render_processor(
    render_json_logs: bool = False,
    serializer: Callable[..., str | bytes] = serialize_to_json,
    colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer(serializer=serializer)
    return structlog.dev.ConsoleRenderer(colors=colors)


def sqlalchemy_processor(_, __, event_dict: structlog.types.EventDict) -> structlog.types.EventDict:
    if event_dict.get('logger') == 'sqlalchemy.engine.Engine':
        event_dict['logger'] = 'sql'
    return event_dict


def drop_color_message_key(_, __, event_dict: structlog.types.EventDict) -> structlog.types.EventDict:
    """
    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.
    """
    event_dict.pop('color_message', None)
    return event_dict
