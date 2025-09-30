async def test_add_booking(db, authenticated_ac):
    rooms_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
                "room_id": rooms_id,
                "date_frome": "2024-01-12",
                "date_to": "2024-02-03"
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert "data" in res