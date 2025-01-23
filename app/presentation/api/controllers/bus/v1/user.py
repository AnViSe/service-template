import logging

from dishka import FromDishka
from faststream.redis import RedisRouter, StreamSub

from app.core.config import config
from app.infrastructure.usecases.usecases import Services
from app.domain.user.dto import UserFullDto

logger = logging.getLogger('sub.user')

user_router = RedisRouter()


@user_router.subscriber(
    stream=StreamSub(
        'user_created',
        group=config.app.bus_group,
        consumer=config.app.consumer_name(),
    )
)
async def user_created(
    msg: UserFullDto,
    service: FromDishka[Services],
):
    logger.debug(msg)
    user = await service.user.get_one(msg.id)
    logger.debug(user)
