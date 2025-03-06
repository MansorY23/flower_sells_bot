from aiogram import Bot
from aiogram.types import BotCommand
from flower_bot.locales import main_menu_ru


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in main_menu_ru.items()
    ]
    await bot.set_my_commands(main_menu_commands)