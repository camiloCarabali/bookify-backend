from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.category import book_category


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("bookify_schema.users.id"))

    uploader = relationship("User", back_populates="books")
    audiobooks = relationship("Audiobook", back_populates="book")
    favorites = relationship("Favorite", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    categories = relationship("Category", secondary=book_category, back_populates="books")
