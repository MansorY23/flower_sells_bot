import sqlalchemy
from sqlalchemy.sql import func

from flower_bot.models.db.flower_point_model import FlowerPoint
from flower_bot.models.db.order_model import Order
from flower_bot.models.db.product_flower_point_model import product_flower_point
from flower_bot.repository.base_repository import BaseRepository


class FlowerPointRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    async def get_all_points(self):
        stmt = sqlalchemy.select(FlowerPoint)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()

    async def get_point_info_by_id(self, point_id: int) -> FlowerPoint:
        stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == point_id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"FlowerPoint with id {id} does not exist")
        return query.scalar()
    
    async def get_income_by_point(self, point_id: int):
        stmt = sqlalchemy.select(func.sum(Order.order_sum))\
            .select_from(Order, FlowerPoint)\
            .join(Order, Order.flower_point_id == FlowerPoint.id )\
            .group_by(FlowerPoint.id) \
            .where(FlowerPoint.id == point_id)
        
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"FlowerPoint with id {id} does not exist")
        return query.scalar()
  
    
    async def get_remained_flowers_by_point(self, point_id: int):
        stmt = sqlalchemy.select(func.sum(product_flower_point.c.quantity))\
            .select_from(product_flower_point, FlowerPoint)\
            .join(product_flower_point, product_flower_point.c.flower_point_id == FlowerPoint.id)\
            .group_by(FlowerPoint.id) \
            .where(FlowerPoint.id == point_id)
        
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"FlowerPoint with id {id} does not exist")
        return query.scalar()
    
    async def get_remained_flowers_by_point_name(self, point_id: int):
        stmt = sqlalchemy.select(func.sum(product_flower_point.c.quantity))\
            .select_from(product_flower_point, FlowerPoint)\
            .join(product_flower_point, product_flower_point.c.flower_point_id == FlowerPoint.id)\
            .group_by(FlowerPoint.id) \
            .where(FlowerPoint.id == point_id)
        
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"FlowerPoint with id {id} does not exist")
        return query.scalar()
    
    async def delete_flower_point_by_id(self, flower_point_id: int) -> str:
        select_stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == flower_point_id)
        query = await self.session.execute(statement=select_stmt)
        delete_flower_point = query.scalar()

        if not delete_flower_point:
            raise Exception(f"Profession with id: {id} does not exist")

        await self.session.delete(delete_flower_point)
        await self.session.flush()
        await self.session.commit()
        return f"flower_point with id {delete_flower_point.id} successfully deleted"

    async def create_new_flower_point(self, address: int) -> FlowerPoint:
        new_flower_point = FlowerPoint(address=address)
        self.session.add(instance=new_flower_point)
        await self.session.flush()
        await self.session.refresh(instance=new_flower_point)
        await self.session.commit()
        return new_flower_point
    
    async def get_point_by_user(self, user_id: int):
        stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == user_id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"User with id {id} does not exist")
        return query.scalar()
    
    """ 
    async def update_flower_point_name(self, id: int, name: str):
        select_stmt = sqlalchemy.select(FlowerPoint).where(FlowerPoint.id == id)
        query = await self.session.execute(statement=select_stmt)
        update_flower_point = query.scalar()

        if not update_flower_point:
            raise Exception(f"flower_point with id {id} does not exist")

        update_stmt = sqlalchemy.update(table=FlowerPoint)\
            .where(FlowerPoint.id == update_flower_point.id).values(name=name, updated_at=functions.now())

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update_flower_point)
    """