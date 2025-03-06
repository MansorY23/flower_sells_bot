from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import MetaData, DateTime, schema
from sqlalchemy.sql import functions


class Base(DeclarativeBase):
    metadata: MetaData = MetaData(schema='public')


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=True, server_default=functions.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True,
        server_onupdate=schema.FetchedValue(for_update=True))