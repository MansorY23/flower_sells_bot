from sqlalchemy import ForeignKey, Integer, ForeignKeyConstraint, Table, Column
#from sqlalchemy.orm import Mapped, mapped_column

#from flower_bot.models.db.flower_point_model import FlowerPoint
#from flower_bot.models.db.product_model import Product
from flower_bot.models.db.base_model import BaseModel


"""
class ProductFlowerPoint(BaseModel):
    __tablename__ = "product_flower_point"

    flower_point_id: Mapped[int] =  mapped_column(
        ForeignKey('flower_point.id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    __table_args__ = (ForeignKeyConstraint([flower_point_id, product_id],
                                           [FlowerPoint.flower_point_id, Product.product_id]),
                                           {})
"""
product_flower_point = Table(
    "product_flower_point",
    BaseModel.metadata,
    Column("flower_point_id", ForeignKey("flower_point.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=0)

)