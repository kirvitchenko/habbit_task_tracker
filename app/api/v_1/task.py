from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task import TaskUpdateSchema, TaskViewSchema
from app.services.task import TaskService
from app.utils.depends import get_async_db

router = APIRouter(prefix='/api/v1/tasks')

@router.post('/', response_model=TaskViewSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskUpdateSchema, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.create_task(task_data=task_data, db=db)


@router.get('/{task_id}', response_model=TaskViewSchema)
async def retrieve_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.retrieve_task(db=db, task_id=task_id)

@router.patch('/{task_id}', response_model=TaskViewSchema, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task_data: TaskUpdateSchema, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.update_task(db=db, task_id=task_id, task_data=task_data)

@router.delete('/{task_id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.delete_task(db=db, task_id=task_id)

@router.post('/{task_id}/start', response_model=TaskViewSchema, status_code=status.HTTP_200_OK)
async def processed_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.processed_task(db=db, task_id=task_id)

@router.post('/{task_id}/done', response_model=TaskViewSchema, status_code=status.HTTP_200_OK)
async def done_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    return await TaskService.done_task(db=db, task_id=task_id)

