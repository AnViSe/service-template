from faststream.redis import RedisRouter

from .v1 import user_router

router_bus = RedisRouter()
router_bus.include_router(user_router)
