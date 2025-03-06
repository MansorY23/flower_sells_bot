from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flower_bot.models.db.base_model import BaseModel


class Order(BaseModel):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    order_sum: Mapped[int] = mapped_column(Integer, nullable=False) 

    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='NO ACTION'), nullable=True)
    flower_point_id: Mapped[int] = mapped_column(
        ForeignKey('flower_point.id', ondelete='NO ACTION'), nullable=False)
    flower_point: Mapped['FlowerPoint'] = relationship(back_populates='orders')