from pydantic import BaseModel
from typing import Optional, List
from app.schemas.category import CategoryOut


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class BookCreate(BookBase):
    category_ids: List[int] = []


class BookOut(BookBase):
    id: int
    uploaded_by: Optional[int]
    categories: List[CategoryOut] = []
    audiobooks: Optional[List["AudiobookOut"]] = []

    class Config:
        from_attributes = True


class AudiobookOut(BaseModel):
    id: int
    file_path: str
    book_id: int


BookOut.model_rebuild()
