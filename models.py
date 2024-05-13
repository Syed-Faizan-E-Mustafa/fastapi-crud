import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(30), unique=True)
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = 'items'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")
