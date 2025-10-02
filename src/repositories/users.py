from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, user_email: EmailStr):
        query = select(self.model).filter_by(email=user_email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
    async def add(self, data: BaseModel):
        try:
            add_data_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            result = await self.session.execute(add_data_stmt)
            self.model = result.scalars().one()
            return self.mapper.map_to_domain_entity(self.model)
        except IntegrityError:
            raise HTTPException(
                status_code=409, 
                detail="Пользователь с таким email уже существует"
            )
