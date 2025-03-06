from sqlalchemy import ForeignKey, Table, Column
from flower_bot.models.db.base_model import BaseModel


order_product: Table = Table(
    'order_product',
    BaseModel.metadata,
    Column('order_id', ForeignKey('order.id')),
    Column('product_id', ForeignKey('product.id'))
)