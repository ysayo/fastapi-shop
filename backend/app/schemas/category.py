from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100,
        description="Category name")
    slug: str = Field(..., min_length=5, max_length=100,
        description="URL-friendly category name")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description='Unique category identifier')
    # Локализованные названия (могут быть None, если перевод ещё не сделан)
    name_ru: Optional[str] = None
    name_en: Optional[str] = None

    class Config:
        from_attributes = True
