from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, PaginathionDep
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    db: DBDep,
    paginathion: PaginathionDep,
    title: str | None = Query(None, description="Название"),
    location: str | None = Query(None, description="Локация"),
):
    per_page = paginathion.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (paginathion.page - 1),
    )


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.post("")
async def create_hotel(db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Крутой отель Сочи", "location": "бест хотел нейм"},
            }
        }
    )
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
    await db.hotels.edit(
        hotel_data, exclude_unset=True, id=hotel_id
    )
    await db.commit()
    return {"status": "ok"}


@router.get("/{hotel_id}")
async def get_hotel_by_id(db: DBDep,hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)
