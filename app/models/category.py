from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("bookify_schema.books.id")),
    Column("category_id", Integer, ForeignKey("bookify_schema.categories.id")),
    schema="bookify_schema"
)


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship("Book", secondary=book_category, back_populates="categories")
