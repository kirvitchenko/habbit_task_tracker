"""Endpoints for tasks"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, status

from app.models.task import TaskStatusChoices
from app.schemas.task import TaskUpdateSchema, TaskViewSchema, TaskFiltersSchema
from app.utils.depends import TaskServiceDep

router = APIRouter(prefix="/tasks")


@router.post("/", response_model=TaskViewSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskUpdateSchema, service: TaskServiceDep):
    """Create a task"""
    return await service.create_task(task_data=task_data)


@router.get("/", response_model=List[TaskViewSchema])
async def list_task(
    service: TaskServiceDep,
    task_status: Optional[TaskStatusChoices] = None,
    due_date: Optional[date] = None,
    deadline: Optional[date] = None,
):
    """Get a list of tasks"""
    filters = TaskFiltersSchema(
        due_date=due_date, deadline=deadline, status=task_status
    )
    return await service.list_task(filters=filters)


@router.get("/{task_id}", response_model=TaskViewSchema)
async def retrieve_task(task_id: int, service: TaskServiceDep):
    """Get a category"""
    return await service.get_by_id(task_id=task_id)


@router.patch(
    "/{task_id}", response_model=TaskViewSchema, status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: int, task_data: TaskUpdateSchema, service: TaskServiceDep
):
    """Update a task"""
    return await service.update_task(task_id=task_id, task_data=task_data)


@router.delete("/{task_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, service: TaskServiceDep):
    return await service.delete_task(task_id=task_id)


@router.post(
    "/{task_id}/start", response_model=TaskViewSchema, status_code=status.HTTP_200_OK
)
async def processed_task(task_id: int, service: TaskServiceDep):
    """Change task status to 'in process'"""
    task_status = TaskStatusChoices.in_process
    return await service.change_status(task_id=task_id, status=task_status)


@router.post(
    "/{task_id}/done", response_model=TaskViewSchema, status_code=status.HTTP_200_OK
)
async def done_task(task_id: int, service: TaskServiceDep):
    """Change task status to 'done'"""
    task_status = TaskStatusChoices.done
    return await service.change_status(task_id=task_id, status=task_status)
