import sqlalchemy
from sqlalchemy.sql import func, functions

from flower_bot.models.db.flower_point_model import FlowerPoint
from flower_bot.models.db.product_flower_point_model import product_flower_point
from flower_bot.repository.base_repository import BaseRepository


class ProductFlowerPointRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    async def get_all_points(self):
        stmt = sqlalchemy.select()
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()
    
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

    async def get_remained_flowers_all_points(self):
        stmt = sqlalchemy.select(func.sum(product_flower_point.c.quantity))
            #.select_from(product_flower_point)\
        
        query = await self.session.execute(statement=stmt)
        if not query:
            raise Exception(f"Error happened. There is no data")
        return query.scalar()

    #async def create_new_relation(self):
    #    #self.session.add(instance=)
    #    await self.session.flush()
    #    await self.session.commit()
    #    await self.session.refresh(instance=new_flower_point)
    #    return new_flower_point


    async def update_stock(self, point_id: int,
                                     product_id: int, new_quantity: int):
        
        #select_stmt = sqlalchemy.select(product_flower_point)\
        #    .where(product_flower_point.c.flower_point_id == point_id, 
        #          product_flower_point.c.product_id == product_id)
        #query = await self.session.execute(statement=select_stmt)
        #exact_stock = query.scalar()

        #if not exact_stock:
        #    raise Exception(f"order with id {id} does not exist")

        update_stmt = sqlalchemy.update(table=product_flower_point)\
            .where(product_flower_point.c.flower_point_id == point_id, 
                  product_flower_point.c.product_id == product_id)\
            .values(quantity=new_quantity)
        query = await self.session.execute(statement=update_stmt)
        

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        #await self.session.refresh(exact_stock)
