from pydantic import BaseModel
from typing import Optional, List
from app.schemas.category import CategoryOut


class AudioBookBase(BaseModel):
    audio_url: str


class AudioBookOut(AudioBookBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    category_ids: Optional[List[int]] = []


class BookCreate(BookBase):
    audio_url: Optional[str] = None


class BookOut(BookBase):
    id: int
    uploaded_by: Optional[int]
    audiobook: Optional[AudioBookOut] = None
    categories: List[CategoryOut] = []

    class Config:
        orm_mode = True
