from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True, index=True)
    comentario = Column(String, nullable=False)
    calificacion = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("bookify_schema.users.id"))
    book_id = Column(Integer, ForeignKey("bookify_schema.books.id"))

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
