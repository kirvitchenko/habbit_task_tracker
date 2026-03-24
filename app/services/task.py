from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskModel, TaskStatusChoices
from app.schemas.task import TaskUpdateSchema
from app.utils.exceptions import NotFoundError


class TaskService:
    @staticmethod
    async def create_task(task_body: TaskUpdateSchema, session: AsyncSession):
        task = TaskModel(**task_body.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def retrieve_task(session: AsyncSession, task_id: int):
        result = await session.execute(
            select(TaskModel).filter(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        return task

    @staticmethod
    async def update_task(
        session: AsyncSession, task_id: int, task_body: TaskUpdateSchema
    ):
        result = await session.execute(
            select(TaskModel).filter(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")

        update_data = task_body.model_dump(exclude_unset=True)
        for field, value in update_data:
            setattr(task, field, value)

        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int):
        result = await session.execute(
            select(TaskModel).filter(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def processed_task(session: AsyncSession, task_id: int):
        result = await session.execute(
            select(TaskModel).filter(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        task.status = TaskStatusChoices.in_process
        await session.commit()

    @staticmethod
    async def done_task(session: AsyncSession, task_id: int):
        result = await session.execute(
            select(TaskModel).filter(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        task.status = TaskStatusChoices.done
        await session.commit()

    @staticmethod
    async def filtered_tasks(
        session: AsyncSession, status: TaskStatusChoices, due_date: date, deadline: date
    ):
        stmt = select(TaskModel)

        if status:
            stmt = stmt.filter(TaskModel.status == status)
        if due_date:
            stmt = stmt.filter(TaskModel.due_date == due_date)
        if deadline:
            stmt = stmt.filter(TaskModel.deadline == deadline)

        result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks
