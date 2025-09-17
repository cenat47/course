from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from schemas.rooms import RoomWithRels, Rooms
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all_by_time(self, hotel_id, date_to, date_from):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        query = (select(self.model)
                .options(joinedload(self.model.facilities))
                .filter(RoomsOrm.id.in_(rooms_ids_to_get))
                )
        result = await self.session.execute(query)
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).options(joinedload(self.model.facilities))
        result = await self.session.execute(query)
        model = result.scalars().unique().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)