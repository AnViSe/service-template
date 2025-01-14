from fastapi import APIRouter

from app.controllers.http.v1 import permission

router = APIRouter()
router.include_router(permission.router)
