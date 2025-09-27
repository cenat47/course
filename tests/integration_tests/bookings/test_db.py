from src.schemas.bookings import BookingsAddToDB


async def test_crud_booking(db):
    user_id = (await db.users.get_all())[0].id
    rooms_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAddToDB(
        user_id=user_id,
        room_id=rooms_id,
        date_frome="2023-12-12",
        date_to="2024-01-01",
        create_at="2023-01-01",
        price="100",
    )

    booking_data_edit = BookingsAddToDB(
        user_id=user_id,
        room_id=rooms_id,
        date_frome="2023-12-12",
        date_to="2024-01-01",
        create_at="2023-01-01",
        price="200",
    )

    bookings = await db.bookings.add(booking_data)
    bookings_select = await db.bookings.get_one_or_none(id=bookings.id)
    assert bookings_select

    bookings_update = await db.bookings.edit(booking_data_edit)
    assert bookings_update.price == 200

    await db.bookings.delete(id=bookings.id)
    bookings_select = await db.bookings.get_one_or_none(id=bookings.id)
    assert not bookings_select

    await db.commit()
