from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Audiobook(Base):
    __tablename__ = "audiobooks"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey("bookify_schema.books.id"), nullable=False)

    book = relationship("Book", back_populates="audiobooks")
