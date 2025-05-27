from pydantic import BaseModel, Field, conint


class ReviewBase(BaseModel):
    comentario: str = Field(..., min_length=5, max_length=1000)
    calificacion: conint(ge=1, le=5)


class ReviewCreate(ReviewBase):
    book_id: int


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    book_id: int

    class Config:
        orm_mode = True
