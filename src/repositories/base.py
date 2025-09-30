from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*filter)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        self.model = result.scalars().one()
        return self.mapper.map_to_domain_entity(self.model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit_bulk(self, data: list[BaseModel]):
        for item in data:
            stmt = (
                update(self.model)
                .where(self.model.id == item.id)
                .values(**item.model_dump())
            )
            await self.session.execute(stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        edit_data_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(edit_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
