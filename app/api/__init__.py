from fastapi import APIRouter

from app.api.v_1 import router as v1_router

router = APIRouter(prefix='/api')
router.include_router(v1_router)
__all__ = ['v1_router', 'router']
