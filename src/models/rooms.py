from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,relationship,  mapped_column

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = "Rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("Hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesOrm"]] = relationship(back_populates="rooms", secondary="Rooms_Facilities")
