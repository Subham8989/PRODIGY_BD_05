from typing import List
from uuid import uuid4
from sqlalchemy import String, Integer, ForeignKey
from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Room(db.Model):
  __tablename__ = "rooms"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  price: Mapped[int] = mapped_column(nullable=True)

  owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
  owner: Mapped["User"] = relationship(back_populates="rooms") # type: ignore

  bookings: Mapped[List["Booking"]] = relationship(back_populates="room") # type: ignore 