"""Services for category"""

from typing import List

from app.cache.service import RedisService
from app.kafka.producer import CategoryKafkaService
from app.models import CategoryModel
from app.repository.category import CategoryRepository
from app.schemas.category import CategoryUpdateSchema, CategoryViewSchema
from app.utils.exceptions import NotFoundError


class CategoryService:
    """Service for category"""

    def __init__(
        self,
        repo: CategoryRepository,
        cache: RedisService,
        producer: CategoryKafkaService,
    ):
        self.repo = repo
        self.cache = cache
        self.producer = producer

    async def _get_category_or_error(self, category_id: int) -> CategoryModel:
        """Get one category"""
        category = await self.repo.get_by_id(category_id=category_id)
        if not category:
            raise NotFoundError(f"Category {category_id} has not been found")
        return category

    async def _cache_and_return(
        self, alchemy_model: CategoryModel
    ) -> CategoryViewSchema:
        """Cache result"""
        pydantic_category_model = CategoryViewSchema.model_validate(alchemy_model)
        await self.cache.set(obj_id=alchemy_model.id, value=pydantic_category_model)
        return pydantic_category_model

    async def get_by_id(self, category_id: int) -> CategoryViewSchema:
        """
        Get one category from cache
        If cache is not exists, get from db and cached, and return
        """
        cached_category = await self.cache.get(category_id)
        if cached_category:
            return cached_category
        alchemy_category_model = await self._get_category_or_error(
            category_id=category_id
        )
        return await self._cache_and_return(alchemy_model=alchemy_category_model)

    async def create_category(
        self, category_data: CategoryUpdateSchema
    ) -> CategoryViewSchema:
        """Create category and update cache"""
        alchemy_category_model = await self.repo.create(category_data=category_data)
        await self.producer.create_category_event(
            category_id=alchemy_category_model.id, category_data=category_data
        )
        return await self._cache_and_return(alchemy_model=alchemy_category_model)

    async def list_category(self) -> List[CategoryViewSchema]:
        """Get list of categories"""
        categories = await self.repo.list()
        return [CategoryViewSchema.model_validate(category) for category in categories]

    async def update_category(
        self, category_id: int, category_data: CategoryUpdateSchema
    ) -> CategoryViewSchema:
        """Update category"""
        category_instance = await self._get_category_or_error(category_id)
        await self.cache.delete(obj_id=category_id)
        alchemy_category_model = await self.repo.update(
            category_data=category_data, category=category_instance
        )
        await self.producer.update_category_event(
            category_id=category_id, category_data=category_data
        )
        return await self._cache_and_return(alchemy_model=alchemy_category_model)

    async def delete_category(self, category_id: int) -> None:
        """Delete category"""
        category = await self._get_category_or_error(category_id=category_id)
        await self.cache.delete(obj_id=category_id)
        await self.repo.delete(category=category)
        await self.producer.delete_category_event(category_id=category_id)
