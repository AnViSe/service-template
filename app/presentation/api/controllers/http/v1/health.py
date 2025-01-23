import logging

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from ping3 import ping

from app.core.config import Config
from app.domain.common.usecases import Services
from .responses.health import HealthStatus, Status

logger = logging.getLogger('http.health')

router = APIRouter(
    prefix='/health',
    tags=['Пульс'],
)


@router.get(
    '',
    response_model=Status,
    status_code=status.HTTP_200_OK,
    description='Get health status',
    summary='Работоспособность сервиса',
)
async def get_health_status(
    config: FromDishka[Config],
):
    return Status(name=f'{config.app.title}: {config.app.version}', status=True)


@router.get(
    '/connections',
    response_model=HealthStatus,
    status_code=status.HTTP_200_OK,
    description='Get connections status',
    summary='Состояние подключений к базам данных',
)
@inject
async def get_health_status(
    config: FromDishka[Config],
    service: FromDishka[Services],
):
    result_status = HealthStatus(statuses=list(), errors=list())
    if config.postgres.host:
        db_ping = ping(config.postgres.host, timeout=1)
        result_status.statuses.append(Status(name='Ping to database server', status=db_ping))
        try:
            main_base_connected = await service.adapters.postgres.check_connection()
            result_status.statuses.append(Status(name='Database server connected', status=main_base_connected))
        except Exception as e:
            result_status.statuses.append(Status(name='Database server not available', status=repr(e)))

    if config.bus.host:
        db_ping = ping(config.bus.host, timeout=1)
        result_status.statuses.append(Status(name='Ping to redis-bus server', status=db_ping))
        try:
            bus_base_connected = await service.adapters.bus.check_connection()
            result_status.statuses.append(Status(name='Redis-bus server connected', status=bus_base_connected))
        except Exception as e:
            result_status.statuses.append(Status(name='Redis-bus not available', status=repr(e)))

    if config.cache.host:
        db_ping = ping(config.cache.host, timeout=1)
        result_status.statuses.append(Status(name='Ping to redis-cache server', status=db_ping))
    return result_status
