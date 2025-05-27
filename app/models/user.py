from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("bookify_schema.roles.id"))
    is_active = Column(Boolean, nullable=False, default=True)

    role = relationship("Role", back_populates="users")
    books = relationship("Book", back_populates="uploader")
    favorites = relationship("Favorite", back_populates="user")
    reviews = relationship("Review", back_populates="user")
