import pytest

from tests.conftest import get_db_null_pool


@pytest.fixture()
async def delete_all_bookings():
    async for db in get_db_null_pool():
        await db.bookings.delete()
        await db.commit()


@pytest.mark.parametrize("room_id, date_frome, date_to, status_code", [
    (1,"2024-01-12", "2024-02-03",200),
    (1,"2024-01-12", "2024-02-03",200),
    (1,"2024-01-12", "2024-02-03",200),
    (1,"2024-01-12", "2024-02-03",200),
    (1,"2024-01-12", "2024-02-03",200),
    (1,"2024-01-12", "2024-02-03",409),
    ])
async def test_add_booking(
    room_id, date_frome, date_to, status_code,
    db, authenticated_ac):
    # rooms_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
                "room_id": room_id,
                "date_frome": date_frome,
                "date_to": date_to
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "data" in res


@pytest.mark.parametrize("room_id, date_frome, date_to, count", [
    (1,"2024-01-12", "2024-02-03",1),
    (1,"2024-01-12", "2024-02-03",2),
    (1,"2024-01-12", "2024-02-03",3),
    ])
async def  test_add_and_get_bookings(delete_all_bookings, db, authenticated_ac, room_id, date_frome, date_to, count,):
    response = await authenticated_ac.post(
        "/bookings",
        json={
                "room_id": room_id,
                "date_frome": date_frome,
                "date_to": date_to
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert "data" in res
    response = await authenticated_ac.get(
        "/bookings/me",
    )
    
    assert response.status_code == 200
    res = response.json()
    len(res) == count
