import json

from fastapi import APIRouter

from app.utils.depends import ClickhouseDashBoardTaskServiceDep

router = APIRouter(prefix="/dashboard")


@router.get("/created_tasks")
async def created_tasks(dashboard_service: ClickhouseDashBoardTaskServiceDep):
    result = await dashboard_service.get_daily_stats()
    return result
