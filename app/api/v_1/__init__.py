from fastapi import APIRouter

from app.api.v_1.category import router as category_router
from app.api.v_1.task import router as task_router

router = APIRouter(prefix="/v1")
router.include_router(category_router)
router.include_router(task_router)

__all__ = ["category_router", "task_router", "router"]
