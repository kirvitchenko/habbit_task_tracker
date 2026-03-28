from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import TaskModel
from app.schemas.task import TaskUpdateSchema, TaskFiltersSchema


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, task_id) -> TaskModel | None:
        task = await self.db.execute(
            select(TaskModel)
            .options(selectinload(TaskModel.category))
            .filter(TaskModel.id == task_id)
        )
        return task.scalar_one_or_none()

    async def create(self, task_data: TaskUpdateSchema) -> TaskModel:
        task = TaskModel(**task_data.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task, attribute_names=["category"])
        return task

    async def list(self, filters: TaskFiltersSchema):
        stmt = select(TaskModel).options(selectinload(TaskModel.category))

        for field, value in filters.model_dump(exclude_unset=True).items():
            stmt = stmt.filter(getattr(TaskModel, field) == value)

        tasks = await self.db.execute(stmt)
        return tasks.scalars().all()

    async def update(self, task: TaskModel, task_data: TaskUpdateSchema) -> TaskModel:
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: TaskModel) -> None:
        await self.db.delete(task)
        await self.db.commit()

    async def save(self, task: TaskModel):
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
