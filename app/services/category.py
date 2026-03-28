from typing import List

from app.cache.service import RedisService
from app.models import CategoryModel
from app.repository.category import CategoryRepository
from app.schemas.category import CategoryUpdateSchema, CategoryViewSchema
from app.utils.exceptions import NotFoundError


class CategoryService:
    def __init__(self, repo: CategoryRepository, cache: RedisService):
        self.repo = repo
        self.cache = cache

    async def _get_category_or_error(self, category_id) -> CategoryModel:
        category = await self.repo.get_by_id(category_id=category_id)
        if not category:
            raise NotFoundError(f"Category {category_id} has not been found")
        return category

    async def get_by_id(self, category_id: int) -> CategoryViewSchema:
        category = await self._get_category_or_error(category_id=category_id)
        return CategoryViewSchema.model_validate(category)

    async def create_category(
        self, category_data: CategoryUpdateSchema
    ) -> CategoryViewSchema:
        category = await self.repo.create(category_data=category_data)
        return CategoryViewSchema.model_validate(category)

    async def list_category(self) -> List[CategoryViewSchema]:
        categories = await self.repo.list()
        return [CategoryViewSchema.model_validate(category) for category in categories]

    async def update_category(
        self, category_id: int, category_data: CategoryUpdateSchema
    ) -> CategoryViewSchema:
        category_instance = await self._get_category_or_error(category_id)
        category = await self.repo.update(
            category_data=category_data, category=category_instance
        )
        return CategoryViewSchema.model_validate(category)

    async def delete_category(self, category_id: int) -> None:
        category = await self._get_category_or_error(category_id=category_id)
        await self.repo.delete(category=category)
