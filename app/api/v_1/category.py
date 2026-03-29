"""Endpoints for category"""

from typing import List

from fastapi import APIRouter, status
from app.schemas.category import CategoryViewSchema, CategoryUpdateSchema
from app.utils.depends import CategoryServiceDep

router = APIRouter(prefix="/categories")


@router.post(
    "/", response_model=CategoryViewSchema, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_data: CategoryUpdateSchema, service: CategoryServiceDep
):
    """Create a category"""
    return await service.create_category(category_data=category_data)


@router.get("/", response_model=List[CategoryViewSchema])
async def list_category(service: CategoryServiceDep):
    """Get a list of categories"""
    return await service.list_category()


@router.get("/{category_id}", response_model=CategoryViewSchema)
async def retrieve_category(category_id: int, service: CategoryServiceDep):
    """Get a category"""
    return await service.get_by_id(category_id=category_id)


@router.patch("/{category_id}", response_model=CategoryViewSchema)
async def update_category(
    category_id: int,
    category_data: CategoryUpdateSchema,
    service: CategoryServiceDep,
):
    """Update a category"""
    return await service.update_category(
        category_id=category_id, category_data=category_data
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, service: CategoryServiceDep):
    """Delete a category"""
    return await service.delete_category(category_id=category_id)
