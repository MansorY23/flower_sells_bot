import typing
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession, AsyncEngine)

from flower_bot.utils.config import DBConfig
from flower_bot.utils import logger


async def create_sa_engine(settings: DBConfig) -> AsyncEngine:
    logger.debug("Initializing SQLAlchemy engine")
    engine = create_async_engine(
        url=settings.db_dsn,
        echo=True,
        echo_pool=settings.db_echo,
        pool_size=settings.db_pool_size,
        pool_pre_ping=settings.db_pool_pre_ping,
        max_overflow=settings.db_max_overflow,
    )
    logger.debug("SQLAlchemy engine has been initialized")
    return engine


def create_pool(settings: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=settings.db_dsn)
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )
    return pool