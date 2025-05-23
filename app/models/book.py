from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("bookify_schema.users.id"))

    uploader = relationship("User", back_populates="books")
    audiobook = relationship("AudioBook", back_populates="book", uselist=False)


class AudioBook(Base):
    __tablename__ = "audiobooks"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True, index=True)
    audio_url = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey("bookify_schema.books.id"))

    book = relationship("Book", back_populates="audiobook")
