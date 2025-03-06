from typing import Optional

import sqlalchemy
from sqlalchemy.sql import func

from flower_bot.models.db.product_model import Product
from flower_bot.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    async def get_all_products(self):
        stmt = sqlalchemy.select(Product)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()


    async def get_price_by_name(self, product_name: str):
        stmt = sqlalchemy.select(Product.price)\
            .where(Product.product_name == product_name)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise Exception(f"Product with name {product_name} does not exist")
        return query.scalar()
    
    async def update_price_by_name(self, product_name: str, new_price: int):
        
        update_stmt = sqlalchemy.update(table=Product)\
            .where(Product.product_name == product_name)\
            .values(price=new_price)
        query = await self.session.execute(statement=update_stmt)
        
        if not query:
            raise Exception(f"Product with name {product_name} does not exist")

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
    """ 
    async def create_new_product(self, amount: int, order_sum: int,
                               point_id: int, product_id: Optional[int]) -> Order:
        
        new_order = Order(amount=amount, order_sum=order_sum, product_id=product_id,
                           flower_point_id=point_id,
                           )
        self.session.add(instance=new_order)
        await self.session.flush()
        await self.session.refresh(instance=new_order)
        await self.session.commit()
        return new_order
    """

