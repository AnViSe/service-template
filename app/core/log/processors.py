import collections
from typing import Any
from uuid import UUID

import orjson
import structlog
from structlog.typing import EventDict, WrappedLogger

ProcessorType = collections.abc.Callable[
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
    # print(data)
    # result = orjson.dumps(data, default=additionally_serialize).decode()
    result = orjson.dumps(data).decode()
    # print(result)
    return result


def get_render_processor(
    render_json_logs: bool = False,
    serializer: collections.abc.Callable[..., str | bytes] = serialize_to_json,
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


class ForcedKeyOrderRenderer(structlog.processors.KeyValueRenderer):
    """Based upon KeyValueRenderer but returns dict instead of string."""

    def __call__(self, _: WrappedLogger, __: str, event_dict: EventDict):
        sorted_dict = self._ordered_items(event_dict)
        return collections.OrderedDict(**{key: value for key, value in sorted_dict})
