from fastapi import Body, Query, APIRouter, Depends
from src.models.hotels import HotelsOrm
from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginathionDep, PaginathionParams
from src.schemas.hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select
from src.database import async_session_maker

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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Крутой отель Сочи", "location": "бест хотел нейм"},
            }
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id - 1] = {
        "id": hotel_id,
        "title": hotel_data.title,
        "name": hotel_data.name,
    }


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="описание",
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    if hotel_data.title is not None:
        hotels[hotel_id - 1]["title"] = hotel_data.title

    if hotel_data.name is not None:
        hotels[hotel_id - 1]["name"] = hotel_data.name
