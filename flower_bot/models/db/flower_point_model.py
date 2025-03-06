from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flower_bot.models.db.base_model import BaseModel
from flower_bot.models.db.order_model import Order
from flower_bot.models.db.product_flower_point_model import product_flower_point
from flower_bot.models.db.product_model import Product
from flower_bot.models.db.user_model import User


class FlowerPoint(BaseModel):
    __tablename__ = "flower_point"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship(back_populates='flower_point')
    
    products: Mapped[list[Product]] = relationship(
        secondary=product_flower_point, back_populates='flower_points'
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates='flower_point')


