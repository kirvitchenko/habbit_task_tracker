"""Repository for category"""

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryModel
from app.schemas.category import CategoryUpdateSchema


class CategoryRepository:
    """Repository class for category"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> CategoryModel | None:
        """
        Get one entity by id
        :param category_id:
        :return CategoryModel | None:
        """
        category = await self.db.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return category.scalar_one_or_none()

    async def create(self, category_data: CategoryUpdateSchema) -> CategoryModel:
        """
        Create one category
        :param category_data:
        :return CategoryModel:
        """
        category = CategoryModel(**category_data.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def list(self) -> List[CategoryModel]:
        """
        Get list of categories
        :return List[CategoryModel]:
        """
        categories = await self.db.execute(select(CategoryModel))
        return categories.scalars().all()

    async def update(
        self, category_data: CategoryUpdateSchema, category: CategoryModel
    ) -> CategoryModel:
        """
        Update category
        :param category_data:
        :param category:
        :return CategoryModel:
        """
        update_data = category_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: CategoryModel) -> None:
        """
        Delete category
        :param category:
        :return None:
        """
        await self.db.delete(category)
        await self.db.commit()
