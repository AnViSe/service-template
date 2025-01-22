from faststream.redis import RedisRouter

from .v1 import user

router = RedisRouter()
router.include_router(user.router)
