from models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from repositories.base import BaseRepository
from schemas.facilities import Facility, RoomFacility



class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility