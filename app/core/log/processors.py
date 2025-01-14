from collections.abc import Callable

import structlog

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]


def get_render_processor(
    render_json_logs: bool = False,
    colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer()
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
