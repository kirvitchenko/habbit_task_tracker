"""Category schemas"""

from datetime import datetime

from pydantic import BaseModel, Field


class BaseCategorySchema(BaseModel):
    """Base schema for Category"""

    title: str = Field(max_length=100, title="Category Title")


class CategoryViewSchema(BaseCategorySchema):
    """View schema for returning category"""

    id: int = Field(..., description="ID")
    created_at: datetime = Field(..., title="Created at")

    class Config:
        from_attributes = True


class CategoryUpdateSchema(BaseCategorySchema):
    """Schema for updating and creating category"""

    pass
