from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    book_id: int


class FavoriteOut(BaseModel):
    id: int
    book_id: int

    class Config:
        orm_mode = True
