from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.redis import RedisRouter

from app.domain.common.usecases import Services

router = RedisRouter()


@router.subscriber(stream='create')
@inject
async def create_user(
    data: str,
    service: FromDishka[Services]
):
    user = await service.user.create(data)
    return user
