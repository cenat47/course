from sqlalchemy import func, select

from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from schemas.rooms import Rooms
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all_by_time(self, hotel_id, date_to, date_from):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id, date_to, date_from)
        return await self.get_all(RoomsOrm.id.in_(rooms_ids_to_get))
