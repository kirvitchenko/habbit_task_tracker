from typing import List

from app.kafka.producer import TaskKafkaService
from app.tasks.notifications import status_change_task
from app.cache.service import RedisService
from app.models.task import TaskModel
from app.repository.task import TaskRepository
from app.schemas.task import TaskUpdateSchema, TaskFiltersSchema, TaskViewSchema
from app.utils.exceptions import NotFoundError


class TaskService:
    def __init__(
        self, repo: TaskRepository, cache: RedisService, producer: TaskKafkaService
    ):
        self.repo = repo
        self.cache = cache
        self.producer = producer

    async def _get_task_or_error(self, task_id: int) -> TaskModel:
        """Get task or error"""
        task = await self.repo.get_by_id(task_id=task_id)
        if not task:
            raise NotFoundError(f"Task {task_id} has not been found")
        return task

    async def _cache_and_return(self, alchemy_model: TaskModel) -> TaskViewSchema:
        """Cache result and return"""
        pydantic_task_model = TaskViewSchema.model_validate(alchemy_model)
        await self.cache.set(obj_id=alchemy_model.id, value=pydantic_task_model)
        return pydantic_task_model

    async def get_by_id(self, task_id: int) -> TaskViewSchema:
        """Get one task by id"""
        cached_task = await self.cache.get(obj_id=task_id)
        if cached_task:
            return cached_task
        alchemy_task_model = await self._get_task_or_error(task_id=task_id)
        return await self._cache_and_return(alchemy_model=alchemy_task_model)

    async def create_task(self, task_data: TaskUpdateSchema) -> TaskViewSchema:
        """Create one task"""
        alchemy_task_model = await self.repo.create(task_data=task_data)
        await self.producer.task_create_event(
            task_id=alchemy_task_model.id, task_data=task_data
        )
        return await self._cache_and_return(alchemy_model=alchemy_task_model)

    async def list_task(self, filters: TaskFiltersSchema) -> List[TaskViewSchema]:
        """Get list of tasks"""
        tasks = await self.repo.list(filters=filters)
        return [TaskViewSchema.model_validate(task) for task in tasks]

    async def update_task(
        self, task_id: int, task_data: TaskUpdateSchema
    ) -> TaskViewSchema:
        """Update task"""
        task_instance = await self._get_task_or_error(task_id=task_id)
        await self.cache.delete(obj_id=task_id)
        alchemy_task_model = await self.repo.update(
            task_data=task_data, task=task_instance
        )
        await self.producer.task_update_event(task_id=task_id, task_data=task_data)
        return await self._cache_and_return(alchemy_model=alchemy_task_model)

    async def delete_task(self, task_id: int) -> None:
        """Delete task"""
        await self.cache.delete(obj_id=task_id)
        task = await self._get_task_or_error(task_id=task_id)
        await self.producer.task_delete_event(task_id=task_id)
        await self.repo.delete(task)

    async def change_status(self, task_id: int, status) -> TaskViewSchema:
        """Change task status"""
        task = await self._get_task_or_error(task_id=task_id)
        old_status = task.status
        task.status = status
        await self.cache.delete(obj_id=task_id)
        alchemy_task_model = await self.repo.save(task)
        status_change_task.delay(
            task_name=alchemy_task_model.title, status=alchemy_task_model.status.value
        )
        await self.producer.task_change_status_event(
            task_id=task_id,
            old_status=old_status.value,
            new_status=alchemy_task_model.status.value,
        )
        return await self._cache_and_return(alchemy_model=alchemy_task_model)
