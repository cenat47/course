from repositories.mappers.base import DataMapper
from schemas.bookings import Bookings
from schemas.facilities import Facility
from schemas.hotels import Hotel
from schemas.rooms import Rooms, RoomWithRels
from schemas.users import User
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
