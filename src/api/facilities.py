from fastapi import APIRouter

from schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.post("/")
async def add_facilities(db: DBDep, data: FacilitiesAdd):
    data_return = await db.facilities.add(data)
    await db.commit()
    return data_return

@router.get("/")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()
