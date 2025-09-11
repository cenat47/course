from sqlalchemy import ForeignKey, String
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

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_frome).days
