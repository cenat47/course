from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import RoomFacility, RoomFacilityPatch


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def replace_facilities(
        self, room_id: int, facilities: list[RoomFacilityPatch]
    ):
        stmt = select(self.model.facility_id).where(self.model.room_id == room_id)
        result = await self.session.execute(stmt)
        current_ids = {row[0] for row in result}

        new_ids = {f.facility_id for f in facilities}

        if current_ids == new_ids:
            return

        ids_to_remove = current_ids - new_ids
        if ids_to_remove:
            await self.session.execute(
                delete(self.model).where(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_remove),
                )
            )

        ids_to_add = new_ids - current_ids
        if ids_to_add:
            rows_to_add = [
                {"room_id": room_id, "facility_id": fid} for fid in ids_to_add
            ]
            await self.session.execute(insert(self.model), rows_to_add)
