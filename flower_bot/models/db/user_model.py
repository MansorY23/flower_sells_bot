from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

#from flower_bot.models.db.flower_point_model import FlowerPoint
from flower_bot.models.db.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    flower_point: Mapped["FlowerPoint"] = relationship(back_populates='user')
    flower_point_id: Mapped[int] = mapped_column(
        ForeignKey('flower_point.id', ondelete='NO ACTION'), nullable=False)
