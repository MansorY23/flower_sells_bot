import sqlalchemy
from sqlalchemy.sql import func

from flower_bot.models.db.flower_point_model import FlowerPoint
from flower_bot.models.db.product_flower_point_model import product_flower_point
from flower_bot.models.db.user_model import User
from flower_bot.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    async def get_all_users(self):
        stmt = sqlalchemy.select(User)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()

    async def get_user_info_by_id(self, user_id: int) -> User:
        stmt = sqlalchemy.select(User).where(User.id == user_id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"FlowerPoint with id {id} does not exist")
        return query.scalar()
        

    
    async def delete_user_by_id(self, user_id: int) -> str:
        select_stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == user_id)
        query = await self.session.execute(statement=select_stmt)
        delete__user = query.scalar()

        if not delete__user:
            raise Exception(f"Profession with id: {id} does not exist")

        await self.session.delete(delete__user)
        await self.session.flush()
        return f"_user with id {delete__user.id} successfully deleted"

    async def create_new_user(self, address: int) -> FlowerPoint:
        new__user = FlowerPoint(address=address)
        self.session.add(instance=new__user)
        await self.session.flush()
        await self.session.refresh(instance=new__user)

        return new__user
    
    async def get_flower_point_by_user(self, telegram_id: int):
        stmt = sqlalchemy.select(User.flower_point_id).where(User.telegram_id == telegram_id)
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"User with id {id} does not exist")
        return query.scalar()
    
    """ 
    async def update_user_name(self, id: int, name: str):
        select_stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == id)
        query = await self.session.execute(statement=select_stmt)
        update__user = query.scalar()

        if not update__user:
            raise Exception(f"_user with id {id} does not exist")

        update_stmt = sqlalchemy.update(table=FlowerPoint)\
            .where(FlowerPoint.id == update__user.id).values(name=name, updated_at=functions.now())

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update__user)
    """