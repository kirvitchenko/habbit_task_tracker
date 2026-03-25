from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskModel, TaskStatusChoices
from app.schemas.task import TaskUpdateSchema
from app.utils.exceptions import NotFoundError


class TaskService:
    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskUpdateSchema):
        task = TaskModel(**task_data.model_dump())
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def retrieve_task(db: AsyncSession, task_id: int):
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        return task

    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdateSchema):
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data:
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int):
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        await db.delete(task)
        await db.commit()

    @staticmethod
    async def processed_task(db: AsyncSession, task_id: int):
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        task.status = TaskStatusChoices.in_process
        await db.commit()

    @staticmethod
    async def done_task(db: AsyncSession, task_id: int):
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        task.status = TaskStatusChoices.done
        await db.commit()

    @staticmethod
    async def list_task(
        db: AsyncSession, status: TaskStatusChoices, due_date: date, deadline: date
    ):
        stmt = select(TaskModel)

        if status:
            stmt = stmt.filter(TaskModel.status == status)
        if due_date:
            stmt = stmt.filter(TaskModel.due_date == due_date)
        if deadline:
            stmt = stmt.filter(TaskModel.deadline == deadline)

        result = await db.execute(stmt)
        tasks = result.scalars().all()
        return tasks
