from sqlalchemy import select
from sqlalchemy.orm import joinedload

from exceptions import IncorrectDate, RoomsIsNotExists
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_all_by_time(self, hotel_id, date_to, date_from):
        if date_from >date_to:
            raise IncorrectDate    
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_to=date_to, date_from=date_from
        )
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).options(joinedload(self.model.facilities))
        result = await self.session.execute(query)
        model = result.scalars().unique().one_or_none()
        if model is None:
            raise RoomsIsNotExists
        return RoomWithRelsDataMapper.map_to_domain_entity(model)
