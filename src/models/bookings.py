from sqlalchemy import Computed, ForeignKey, Integer, String
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "Bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    date_frome: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Integer, Computed('price * (date_to - date_frome)'))
