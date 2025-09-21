from datetime import date

from fastapi import APIRouter, Body

from schemas.facilities import RoomFacilityAdd, RoomFacilityPatch
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPATCH, RoomPATCHRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/")
async def get_rooms_by_hotel(db: DBDep, hotel_id: int, date_from: date, date_to: date):
    return await db.rooms.get_all_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.delete("/{hotel_id}/rooms/{rooms_id}")
async def delete_room(db: DBDep, rooms_id: int):
    await db.rooms.delete(id=rooms_id)
    await db.commit()
    return {"status": "ok"}


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(**room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{rooms_id}")
async def edit_room(db: DBDep, rooms_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(**room_data.model_dump())
    room = await db.rooms.edit(_room_data, id=rooms_id, exclude_unset=True)

    if room_data.facilities_ids is not None:
        facilities = [
            RoomFacilityPatch(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.replace_facilities(room.id, facilities)

    await db.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{rooms_id}")
async def patch_edit_room(
    db: DBDep, rooms_id: int, room_data: RoomPATCHRequest = Body()
):
    room_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPATCH(**room_dict)
    room = await db.rooms.edit(_room_data, id=rooms_id, exclude_unset=True)

    if room_data.facilities_ids is not None:
        facilities = [
            RoomFacilityPatch(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.replace_facilities(room.id, facilities)

    await db.commit()
    return {"status": "ok"}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(db: DBDep, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(id=room_id)
