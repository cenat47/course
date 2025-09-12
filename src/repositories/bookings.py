from sqlalchemy import select

from repositories.base import BaseRepository
from schemas.bookings import BookingsResponse
from src.models.bookings import BookingsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingsResponse