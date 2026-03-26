from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryModel
from app.schemas.category import CategoryUpdateSchema
from app.utils.exceptions import NotFoundError


class CategoryService:
    @staticmethod
    async def get_category_by_id(category_id: int, db: AsyncSession):
        category = await db.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return category.scalar_one_or_none()

    @staticmethod
    async def get_category_or_404(category_id: int, db: AsyncSession):
        category = await CategoryService.get_category_by_id(category_id=category_id, db=db)
        if not category:
            raise NotFoundError(f"Category {category_id} has not been found")
        return category

    @staticmethod
    async def create_category(category_data: CategoryUpdateSchema, db: AsyncSession):
        category = CategoryModel(**category_data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def retrieve_category(category_id: int, db: AsyncSession):
        return await CategoryService.get_category_or_404(category_id=category_id, db=db)

    @staticmethod
    async def list_category(db: AsyncSession):
        categories = await db.execute(select(CategoryModel))
        return categories.scalars().all()

    @staticmethod
    async def update_category(
        category_id: int, category_data: CategoryUpdateSchema, db: AsyncSession
    ):
        category = await CategoryService.get_category_or_404(category_id=category_id, db=db)
        update_data = category_data.model_dump()
        for key, value in update_data.items():
            setattr(category, key, value)

        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete_category(category_id: int, db: AsyncSession):
        category = await CategoryService.get_category_or_404(category_id=category_id, db=db)
        await db.delete(category)
        await db.commit()
