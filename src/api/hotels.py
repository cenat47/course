from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginathionDep
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    paginathion: PaginathionDep,
    date_from: date,
    date_to: date,
    title: str | None = None,
    location: str | None = None,
):
    per_page = paginathion.per_page or 5
    return await db.hotels.get_all_by_time(
        date_from=date_from,
        date_to=date_to,
        limit=per_page,
        offset=per_page * (paginathion.page - 1),
        title=title,
        location=location,
    )


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Крутой отель Сочи", "location": "бест хотел нейм"},
            }
        }
    ),
):
    add_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "ok", "data": add_hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd = Body()):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.get("/{hotel_id}")
async def get_hotel_by_id(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)
