from datetime import datetime

from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAddToDB

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_bookings(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price = room_data.price
    data = BookingsAddToDB(
        **booking_data.model_dump(),
        user_id=user_id,
        price=price,
        create_at=datetime.now(),
    )
    data_return = await db.bookings.add(data, hotel_id=room_data.hotel_id)
    await db.commit()
    return {"data": data_return}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_users_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_all(user_id=user_id)
