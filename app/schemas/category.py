from datetime import datetime

from pydantic import BaseModel, Field


class BaseCategorySchema(BaseModel):
    title: str = Field(max_length=100)


class CategoryViewSchema(BaseCategorySchema):
    id: int
    created_at: datetime


class CategoryUpdateSchema(BaseCategorySchema):
    pass
