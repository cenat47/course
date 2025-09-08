from fastapi import APIRouter
from src.database import async_session_maker
from repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Авторизация и Аунтефикация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {"status": "ok"}