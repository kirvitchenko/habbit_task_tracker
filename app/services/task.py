from typing import List

from app.cache.service import RedisService
from app.models.task import TaskModel
from app.repository.task import TaskRepository
from app.schemas.task import TaskUpdateSchema, TaskFiltersSchema, TaskViewSchema
from app.utils.exceptions import NotFoundError


class TaskService:
    def __init__(self, repo: TaskRepository, cache: RedisService):
        self.repo = repo
        self.cache = cache

    async def _get_task_or_error(self, task_id: int) -> TaskModel:
        task = await self.repo.get_by_id(task_id=task_id)
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        return task

    async def create_task(self, task_data: TaskUpdateSchema) -> TaskViewSchema:
        alchemy_task_model = await self.repo.create(task_data=task_data)
        pydantic_task_model = TaskViewSchema.model_validate(alchemy_task_model)
        await self.cache.set(obj_id=alchemy_task_model.id, value=pydantic_task_model.model_dump(mode='json'))
        return pydantic_task_model

    async def retrieve_task(self, task_id: int) -> TaskViewSchema:
        cached_task = await self.cache.get(obj_id=task_id)
        if cached_task:
            return TaskViewSchema.model_validate(cached_task)
        alchemy_task_model = await self._get_task_or_error(task_id=task_id)
        pydantic_task_model = TaskViewSchema.model_validate(alchemy_task_model)
        await self.cache.set(obj_id=task_id, value=pydantic_task_model.model_dump(mode='json'))
        return pydantic_task_model

    async def update_task(
        self, task_id: int, task_data: TaskUpdateSchema
    ) -> TaskViewSchema:
        task_instance = await self._get_task_or_error(task_id=task_id)
        await self.cache.delete(obj_id=task_id)
        alchemy_task_model = await self.repo.update(task_data=task_data, task=task_instance)
        pydantic_task_model = TaskViewSchema.model_validate(alchemy_task_model)
        await self.cache.set(obj_id=task_id, value=pydantic_task_model.model_dump(mode='json'))
        return pydantic_task_model

    async def delete_task(self, task_id: int) -> None:
        await self.cache.delete(obj_id=task_id)
        task = await self._get_task_or_error(task_id=task_id)
        await self.repo.delete(task)

    async def change_status(self, task_id: int, status) -> TaskViewSchema:
        task = await self._get_task_or_error(task_id=task_id)
        task.status = status
        await self.cache.delete(obj_id=task_id)
        alchemy_task_model = await self.repo.save(task)
        pydantic_task_model = TaskViewSchema.model_validate(alchemy_task_model)
        await self.cache.set(obj_id=task_id, value=pydantic_task_model.model_dump(mode='json'))
        return pydantic_task_model

    async def list_task(self, filters: TaskFiltersSchema) -> List[TaskViewSchema]:
        if not filters:
            cached_tasks = await self.cache.get_list()
            return [TaskViewSchema.model_validate(cached_task) for cached_task in cached_tasks.values()]
        tasks = await self.repo.list(filters=filters)
        return [TaskViewSchema.model_validate(task) for task in tasks]
