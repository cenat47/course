from datetime import date

from pydantic import BaseModel
from sqlalchemy import insert, select
from exceptions import AllRoomsAreBooked, IncorrectDate
from repositories.utils import rooms_ids_for_booking
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_frome == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add(self, data: BaseModel, hotel_id):
        if data.date_frome >data.date_to:
            raise IncorrectDate
        
        rooms_query = rooms_ids_for_booking(data.date_frome, data.date_to, hotel_id=hotel_id)
        result = await self.session.execute(rooms_query)
        available_room_ids = set(result.scalars().all())

        if data.room_id not in available_room_ids:
            raise AllRoomsAreBooked

        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        created_object = result.scalars().one()
        return self.mapper.map_to_domain_entity(created_object)
