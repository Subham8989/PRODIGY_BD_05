from datetime import datetime, timezone
from typing import List
from uuid import uuid4
from ..extensions import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, DateTime

class User(db.Model):
  __tablename__ = "users"

  id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  name: Mapped[str] = mapped_column(String(50), nullable=False)
  username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  age: Mapped[int] = mapped_column(Integer, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  rooms: Mapped[List["Room"]] = relationship(back_populates="owner") # type: ignore
  bookings: Mapped[List["Booking"]] = relationship(back_populates="user") # type: ignore