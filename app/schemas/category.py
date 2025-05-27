from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
