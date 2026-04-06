import json
from datetime import datetime

from aiokafka import AIOKafkaProducer

from app.schemas.category import CategoryUpdateSchema
from app.schemas.task import TaskUpdateSchema


class KafkaService:
    topic = None

    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def _send(self, key: str, value: dict) -> None:
        await self.producer.send(
            topic=self.topic,
            value=json.dumps(value).encode("utf-8"),
            key=key.encode("utf-8"),
        )


class TaskKafkaService(KafkaService):
    topic = "task.events"

    async def task_create_event(
        self, task_id: int, task_data: TaskUpdateSchema
    ) -> None:
        value = {
            "event_type": "task.created",
            "task_id": task_id,
            "task_data": task_data.model_dump(),
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(value=value, key=str(task_id))

    async def task_update_event(
        self, task_id: int, task_data: TaskUpdateSchema
    ) -> None:
        value = {
            "event_type": "task.updated",
            "task_id": task_id,
            "task_data": task_data.model_dump(exclude_unset=True),
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(value=value, key=str(task_id))

    async def task_delete_event(self, task_id: int) -> None:
        value = {
            "event_type": "task.deleted",
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(key=str(task_id), value=value)

    async def task_change_status_event(
        self, task_id: int, old_status: str, new_status: str
    ) -> None:
        value = {
            "event_type": "task.status.changed",
            "task_id": task_id,
            "old_status": old_status,
            "new_status": new_status,
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(key=str(task_id), value=value)


class CategoryKafkaService(KafkaService):
    topic = "category.events"

    async def create_category_event(
        self, category_id: int, category_data: CategoryUpdateSchema
    ) -> None:
        value = {
            "event_type": "category.created",
            "category_id": category_id,
            "category_data": category_data.model_dump(),
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(key=str(category_id), value=value)

    async def update_category_event(
        self, category_id: int, category_data: CategoryUpdateSchema
    ) -> None:
        value = {
            "event_type": "category.updated",
            "category_id": category_id,
            "category_data": category_data.model_dump(exclude_unset=True),
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(key=str(category_id), value=value)

    async def delete_category_event(self, category_id: int) -> None:
        value = {
            "event_type": "category.deleted",
            "category_id": category_id,
            "timestamp": datetime.now().isoformat(),
        }
        await self._send(key=str(category_id), value=value)
