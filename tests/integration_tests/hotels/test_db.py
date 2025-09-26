from schemas.hotels import HotelAdd
from src.database import async_session_maker_null_pull
from utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="hotel 1", location="Sochi m")
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        await db.hotels.add(hotel_data)
        await db.commit()
