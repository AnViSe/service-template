from faststream.redis import RedisRouter

from app.domain.user.handlers import user_router

router_bus = RedisRouter()
router_bus.include_router(user_router)
