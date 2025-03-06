from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flower_bot.models.db.base_model import BaseModel

#from flower_bot.models.db.flower_point_model import FlowerPoint
from flower_bot.models.db.product_flower_point_model import product_flower_point


class Product(BaseModel):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    flower_points: Mapped[list['FlowerPoint']] = relationship(
        secondary=product_flower_point, back_populates='products'
    )



