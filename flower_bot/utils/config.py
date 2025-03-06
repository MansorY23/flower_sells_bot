import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv(find_dotenv())
print(load_dotenv(find_dotenv()))

@dataclass
class DBConfig:
    host: str = os.environ.get('POSTGRES_HOST')
    port: int = os.getenv('POSTGRES_PORT')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    username: str = os.environ.get('POSTGRES_USERNAME')
    database: str = os.getenv('POSTGRES_DB', 'postgres')
    db_driver: str = "postgresql+asyncpg"

    db_pool_size: int = 5
    db_max_overflow: int = 0
    db_echo: bool = False
    db_pool_pre_ping: bool = True

    @property
    def db_dsn(self) -> URL:
        return URL.create(self.db_driver,
                          self.username,
                          self.password,
                          self.host,
                          self.port,
                          self.database)

@dataclass
class RedisConfig:
    port: int = os.environ.get('REDIS_PORT')
    host: str = os.environ.get('REDIS_HOST')
    #password: str = os.environ.get('REDIS_PASSWORD')
    #username: str = os.environ.get('REDIS_USERNAME')
    db: str = os.environ.get("REDIS_DB")
    use_redis: bool = os.environ['USE_REDIS']

    @property
    def db_url(self):
        return f"host:port/password:user"


@dataclass
class BotConfig:
    token: str = os.environ.get('BOT_TOKEN')
    admin_ids: str = os.environ.get('ADMIN_IDS')

    def admins_ids_to_list(self) -> list[int]:
        admin_ids_str = self.admin_ids.split(',')
        admin_ids = [int(i) for i in admin_ids_str]
        return admin_ids