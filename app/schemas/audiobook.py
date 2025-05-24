from pydantic import BaseModel
from typing import Optional


class AudiobookOut(BaseModel):
    id: int
    file_path: str
    book_id: int

    class Config:
        orm_mode = True
