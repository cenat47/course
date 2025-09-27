from schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="hotel 1", location="Sochi m")
    await db.hotels.add(hotel_data)
    await db.commit()
