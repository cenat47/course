from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms_by_hotel(db: DBDep, hotel_id: int):
    return await db.rooms.get_all(hotel_id=hotel_id)


@router.delete("/{hotel_id}/rooms/{rooms_id}")
async def delete_room(db: DBDep, rooms_id: int):
    await db.rooms.delete(id=rooms_id)
    await db.commit()
    return {"status": "ok"}


@router.post("/{hotel_id}/rooms/")
async def create_room(db: DBDep,
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
    add_room = await db.rooms.add(room_data)
    await db.commit()
    return {"status": "ok", "data": add_room}


@router.put("/{hotel_id}/rooms/{rooms_id}")
async def edit_room(db: DBDep, rooms_id: int, room_data: RoomAdd = Body()):
    await db.rooms.edit(room_data, id=rooms_id)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
)
async def patch_room(db: DBDep, room_id: int, room_data: RoomPATCH):
    await db.rooms.edit(room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"status": "ok"}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(db: DBDep, room_id: int):
        return await db.rooms.get_one_or_none(id=room_id)
