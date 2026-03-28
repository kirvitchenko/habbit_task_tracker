from datetime import datetime

from pydantic import BaseModel, Field


class BaseCategorySchema(BaseModel):
    title: str = Field(max_length=100, title="Category Title")


class CategoryViewSchema(BaseCategorySchema):
    id: int = Field(..., description="ID")
    created_at: datetime = Field(..., title="Created at")

    class Config:
        from_attributes = True


class CategoryUpdateSchema(BaseCategorySchema):
    pass
