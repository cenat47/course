from fastapi import APIRouter, Body

from repositories.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomPATCH
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms_by_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.delete("/{hotel_id}/rooms/{rooms_id}")
async def delete_room(rooms_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=rooms_id)
        await session.commit()
        return {"status": "ok"}


@router.post("/{hotel_id}/rooms/")
async def create_room(
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "hotel_id": 26,
                    "title": "Крутой отель Сочи",
                    "description": "бест хотел нейм",
                    "price": 2500.00,
                    "quantity": 10,
                },
            }
        }
    )
):
    async with async_session_maker() as session:
        add_room = await RoomsRepository(session).add(room_data)
        await session.commit()
        return {"status": "ok", "data": add_room}


@router.put("/{hotel_id}/rooms/{rooms_id}")
async def edit_room(rooms_id: int, room_data: RoomAdd = Body()):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=rooms_id)
        await session.commit()
        return {"status": "ok"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
)
async def patch_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
        return {"status": "ok"}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)
