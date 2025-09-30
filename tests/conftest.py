import json
from unittest import mock
import pytest
from httpx import ASGITransport, AsyncClient

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_session_maker_null_pооl, engine_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pооl) as db:
        yield db


@pytest.fixture()
async def db() -> DBManager:  # type: ignore
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


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

    async with DBManager(session_factory=async_session_maker_null_pооl) as db:
        await db.hotels.add_bulk(hotel_models)
        await db.rooms.add_bulk(room_models)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


register_data = {"email": "test@fe.fd", "password": "1234"}


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db, ac):
    await ac.post(url="/auth/register", json=register_data)


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(url="/auth/login", json=register_data)
    assert ac.cookies["access_token"]
    yield ac
