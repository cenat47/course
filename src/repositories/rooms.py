from repositories.base import BaseRepository
from schemas.rooms import Rooms
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms
