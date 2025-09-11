from sqlalchemy import select

from repositories.base import BaseRepository
from schemas.rooms import Rooms
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm

    schema = Rooms

    async def get_all(self, **filter_by) -> list[Rooms]:
        query = select(RoomsOrm).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            Rooms.model_validate(room, from_attributes=True)
            for room in result.scalars().all()
        ]
