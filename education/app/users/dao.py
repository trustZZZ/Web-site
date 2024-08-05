from app.dao.base import *
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
    selection = None

    @classmethod
    async def buy(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == user_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            result.access = True
            await session.commit()
            return result
