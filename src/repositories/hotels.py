from sqlalchemy import select
from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
