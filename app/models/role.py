from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "bookify_schema"}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")
