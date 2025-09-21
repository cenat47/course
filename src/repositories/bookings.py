from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
