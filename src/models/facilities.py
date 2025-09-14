from sqlalchemy import ForeignKey, String
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class FacilitiesOrm(Base):
    __tablename__ = "Facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomsFacilitiesOrm(Base):
    __tablename__ = "Rooms_Facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id:Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    facility_id:Mapped[int] = mapped_column(ForeignKey("Facilities.id"))