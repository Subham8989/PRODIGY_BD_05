from datetime import date
from uuid import uuid4
from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date

class Booking(db.Model):
  __tablename__ = "bookings"

  id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  
  user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
  room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)

  check_in: Mapped[date] = mapped_column(Date, nullable=False)
  check_out: Mapped[date] = mapped_column(Date, nullable=False)

  user: Mapped["User"] = relationship(back_populates="bookings") # type: ignore
  room: Mapped["Room"] = relationship(back_populates="bookings") # type: ignore