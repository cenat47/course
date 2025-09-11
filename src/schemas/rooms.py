from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class Rooms(RoomAdd):
    id: int


class RoomPATCH(BaseModel):
    hotel_id: int = Field(None)
    title: str = Field(None)
    description: str = Field(None)
    price: int = Field(None)
    quantity: int = Field(None)
