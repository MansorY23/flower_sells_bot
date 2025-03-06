import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import Redis, RedisStorage

from flower_bot.db import create_pool
from flower_bot.handlers import admin_panel, commands, sells_handlers
from flower_bot.keyboards import set_main_menu
from flower_bot.middlewares import DBSessionMiddleware
from flower_bot.utils import BotConfig, DBConfig, RedisConfig, logger


async def main():
    logger.info('Starting bot')
    bot_config: BotConfig = BotConfig()
    db_config: DBConfig = DBConfig()
    redis_config = RedisConfig()
    redis: Redis = Redis(host=redis_config.host,
                         port=redis_config.port,
                         db=redis_config.db)
    bot: Bot = Bot(
        token=bot_config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    if redis_config.use_redis is True:
        storage = RedisStorage(redis=redis)
    else:
        storage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(commands.router, sells_handlers.router, admin_panel.router)

    dp.update.middleware(DBSessionMiddleware(session_pool=create_pool(db_config)))
    dp.workflow_data.update({'admin_ids': bot_config.admins_ids_to_list()})
    print(bot_config.admins_ids_to_list())
    await set_main_menu(bot=bot)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())