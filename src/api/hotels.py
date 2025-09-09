from fastapi import APIRouter, Body, Query

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginathionDep
from src.database import async_session_maker
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    paginathion: PaginathionDep,
    title: str | None = Query(None, description="Название"),
    location: str | None = Query(None, description="Локация"),
):
    per_page = paginathion.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (paginathion.page - 1),
        )


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.post("")
async def create_hotel(
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Крутой отель Сочи", "location": "бест хотел нейм"},
            }
        }
    )
):
    async with async_session_maker() as session:
        add_hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "ok", "data": add_hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd = Body()):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()
        return {"status": "ok"}


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)
