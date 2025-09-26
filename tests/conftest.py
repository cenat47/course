import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.database import Base, async_session_maker_null_pull, engine_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_test_mode):
    with open("tests\mock_hotels.json", "r", encoding="utf-8") as f:
        hotel_data = json.load(f)
    with open("tests\mock_rooms.json", "r", encoding="utf-8") as f:
        rooms_data = json.load(f)
    hotel_models = [HotelAdd(**item) for item in hotel_data]
    room_models = [RoomAdd(**item) for item in rooms_data]

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        await db.hotels.add_bulk(hotel_models)
        await db.rooms.add_bulk(room_models)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            url="/auth/register", json={"email": "test@fe.fd", "password": "1234"}
        )
