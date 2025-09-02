from  fastapi import  Body, Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "ван"},
    {"id": 2, "title": "Дубай", "name": "ту"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]




@router.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}

@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={"1":{"summary":"Сочи", "value":{"title": "Крутой отель Сочи", "name": "бест хотел нейм"}}})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"]+1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })



@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id-1] = {
        "id": hotel_id,
        "title": hotel_data.title,
        "name": hotel_data.name}

@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле", description="описание")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    if hotel_data.title is not None:
        hotels[hotel_id-1]["title"] = hotel_data.title
    
    if hotel_data.name is not None:
        hotels[hotel_id-1]["name"] = hotel_data.name

