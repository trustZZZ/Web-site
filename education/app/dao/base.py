from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.tutorials.models import Themes
from app.users.schemas import SUserID
from app.tutorials.schemas import SBlocks


class BaseDAO:
    model = None
    selection = None


    @classmethod
    async def find_by_id(cls, user_id: int) -> SUserID:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=user_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            result_dto = SUserID.model_validate(result, from_attributes=True)
            return result_dto

    @classmethod
    async def find_all(cls, **filter_by) -> SBlocks:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).options(selectinload(cls.selection))
            result = await session.execute(query)
            result = result.unique().scalars().all()
            # result_dto = SBlocks.model_validate(result, from_attributes=True)
            return result

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_and_update(cls, params: dict, **filter_by):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**filter_by).values(params)
            result = await session.execute(query)
            await session.commit()
            return result
            

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
