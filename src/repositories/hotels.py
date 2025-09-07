from sqlalchemy import select
from repositories.base import BaseRepository
from schemas.hotels import Hotel
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
    async def get_all(self, location, title, limit, offset) ->list[Hotel]:
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
