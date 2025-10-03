from datetime import date, datetime

from pydantic import BaseModel, Field


class BookingsAddRequest(BaseModel):
    room_id: int
    date_frome: date
    date_to: date


class BookingsAddToDB(BookingsAddRequest):
    user_id: int
    price: int
    create_at: datetime


class BookingsResponse(BookingsAddToDB):
    id: int
    total_cost: int


class Bookings(BookingsResponse): ...


class BookingsPATCH(BaseModel):
    id: int = Field(None)
    user_id: int = Field(None)
    room_id: int = Field(None)
    date_frome: date = Field(None)
    date_to: date = Field(None)
    price: int = Field(None)
