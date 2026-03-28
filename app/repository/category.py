from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryModel
from app.schemas.category import CategoryUpdateSchema


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id):
        category = await self.db.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return category.scalar_one_or_none()

    async def create(self, category_data: CategoryUpdateSchema):
        category = CategoryModel(**category_data.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def list(self):
        categories = await self.db.execute(select(CategoryModel))
        return categories.scalars().all()

    async def update(
        self, category_data: CategoryUpdateSchema, category: CategoryModel
    ):
        update_data = category_data.model_dump()
        for key, value in update_data.items():
            setattr(category, key, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: CategoryModel):
        await self.db.delete(category)
        await self.db.commit()
