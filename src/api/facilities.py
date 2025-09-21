import json
from fastapi import APIRouter

from schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep
from src.init import redis_manager
router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("/")
async def add_facilities(db: DBDep, data: FacilitiesAdd):
    data_return = await db.facilities.add(data)
    await db.commit()
    return data_return


@router.get("/")
async def get_all_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schema: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities",facilities_json,5)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts
