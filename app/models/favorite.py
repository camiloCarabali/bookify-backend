from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uix_user_book"),
        {"schema": "bookify_schema"}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("bookify_schema.users.id"))
    book_id = Column(Integer, ForeignKey("bookify_schema.books.id"))

    user = relationship("User", back_populates="favorites")
    book = relationship("Book", back_populates="favorites")
