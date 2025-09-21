from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "Facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities", secondary="Rooms_Facilities"
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = "Rooms_Facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("Facilities.id"))
