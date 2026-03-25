from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.category import CategoryViewSchema, CategoryUpdateSchema
from app.services.category import CategoryService
from app.utils.depends import get_async_db

router = APIRouter(prefix='/categories')

@router.post('/', response_model=CategoryViewSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryUpdateSchema, db: AsyncSession = Depends(get_async_db)):
    return await CategoryService.create_category(category_data=category_data, db=db)

@router.get('/', response_model=List[CategoryViewSchema])
async def list_category(db: AsyncSession = Depends(get_async_db)):
    return await CategoryService.list_category(db=db)

@router.get('/{category_id}', response_model=CategoryViewSchema)
async def retrieve_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    return await CategoryService.retrieve_category(category_id=category_id, db=db)

@router.patch('/{category_id}', response_model=CategoryViewSchema)
async def update_category(category_id: int, category_data: CategoryUpdateSchema, db: AsyncSession = Depends(get_async_db)):
    return await CategoryService.update_category(category_id=category_id, category_data=category_data, db=db)

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    return await CategoryService.delete_category(category_id=category_id, db=db)
