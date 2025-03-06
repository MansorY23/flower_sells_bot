from typing import Optional

import sqlalchemy
from sqlalchemy.sql import func

from flower_bot.models.db.order_model import Order
from flower_bot.repository.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    async def select_all(self):
        stmt = sqlalchemy.select(Order)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()

    async def select_orders_by_point(self, point_id: int):
        stmt = sqlalchemy.select(Order).where(Order.flower_point_id == point_id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"Flower point with id {id} does not exist")
        return query.scalars().all()

    async def select_order_by_id(self, order_id: int):
        stmt = sqlalchemy.select(Order).where(Order.id == order_id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"Order with id {id} does not exist")
        return query.scalar()

    async def create_new_order(self, amount: int, order_sum: int,
                               point_id: int, product_id: Optional[int]) -> Order:
        
        new_order = Order(amount=amount, order_sum=order_sum, product_id=product_id,
                           flower_point_id=point_id,
                           )
        self.session.add(instance=new_order)
        await self.session.flush()
        await self.session.refresh(instance=new_order)
        await self.session.commit()
        return new_order
    
    async def get_income_from_all_points(self):
        stmt = sqlalchemy.select(func.sum(Order.order_sum))\
            .select_from(Order)
        
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"Some mistage happen, there are no data")
        return query.scalar()
    

    """ 
    async def delete_order_by_id(self, order_id: int) -> str:
        select_stmt = sqlalchemy.select(Order).where(Order.id == order_id)
        query = await self.session.execute(statement=select_stmt)
        delete_order = query.scalar()

        if not delete_order:
            raise Exception(f"Profession with id: {id} does not exist")

        await self.session.delete(delete_order)
        await self.session.flush()
        await self.session.commit()

        return f"order with id {delete_order.id} successfully deleted"
    """