from  fastapi import  Body, FastAPI, Query
import  uvicorn
app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "ван"},
    {"id": 2, "title": "Дубай", "name": "ту"},
]

@app.get("/hotels")
def get_hotels(
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля")
):
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"]+1,
        "title": title
    })





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
