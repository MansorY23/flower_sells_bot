from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup)


def create_user_reply_kb() -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = list()
    buttons.append(KeyboardButton(text='Статистика'))
    buttons.append(KeyboardButton(text='Добавить продажу'))
    kb_builder.row(*buttons, width=2)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(is_persistent=True, resize_keyboard=True)