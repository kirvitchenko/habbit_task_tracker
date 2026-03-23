from pydantic import BaseModel, Field


class BaseCategorySchema(BaseModel):
    name: str = Field(max_length=100)

class CategoryViewSchema(BaseCategorySchema):
    id: int

class CategoryUpdateSchema(BaseCategorySchema):
    pass