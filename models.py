from database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
#  alembic init migrations
#  alembic revision
#  alembic revision --autogenerate
#  alembic upgrade head


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, index=True)
    hash_password = Column(String(150))
    email = Column(String(150), unique=True)
    full_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_update = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("Item", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    number = Column(Integer, default=0)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="items")
