from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomAddRequest(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None

class Rooms(RoomAdd):
    id: int


class RoomPATCH(BaseModel):
    hotel_id: int = Field(None)
    title: str = Field(None)
    description: str = Field(None)
    price: int = Field(None)
    quantity: int = Field(None)


class RoomPATCHRequest(BaseModel):
    hotel_id: int = Field(None)
    title: str = Field(None)
    description: str = Field(None)
    price: int = Field(None)
    quantity: int = Field(None)
    facilities_ids: list[int] = Field(None)
