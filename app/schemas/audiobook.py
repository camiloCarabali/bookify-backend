from pydantic import BaseModel


class AudiobookOut(BaseModel):
    id: int
    file_path: str
    book_id: int

    class Config:
        orm_mode = True
