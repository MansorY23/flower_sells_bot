from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


class AmountCallbackFactory(CallbackData, prefix='amount'):
    amount: int


def create_start_work_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    buttons.append(InlineKeyboardButton(
        callback_data='start_work',
        text='Начать работу'
    ))
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_sale_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    buttons.append(InlineKeyboardButton(
        callback_data='add_sale',
        text='Добавить')
        )
    buttons.append(InlineKeyboardButton(
        callback_data='cancel',
        text='Отмена')
        )
    kb_builder.row(*buttons, width=2)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_number_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    for num in range(12):
        if num % 2 != 0:
            buttons.append(InlineKeyboardButton(text=f'{num}', 
                                                callback_data=AmountCallbackFactory(amount=num).pack())
                                                )
    

    kb_builder.row(*buttons, width=3)
    kb_builder.row(InlineKeyboardButton(callback_data='cancel',text='Отмена'),
                    InlineKeyboardButton(callback_data='entry_manual',text='Ввод вручную'), 
                    width=2)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_payment_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    buttons.append(InlineKeyboardButton(
        callback_data='transfer',
        text='Перевод'
    ))
    buttons.append(InlineKeyboardButton(
        callback_data='cash',
        text='Наличка'
    ))  
    kb_builder.row(*buttons, width=2)

    kb_builder.row(InlineKeyboardButton(
        callback_data='cancel',
        text='Отмена'
        ))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_confirm_keyboard()-> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    buttons.append(InlineKeyboardButton(
        callback_data='confirm',
        text='Подтвердить'
    ))
    buttons.append(InlineKeyboardButton(
        callback_data='cash',
        text='Отмена'
    ))  
    kb_builder.row(*buttons, width=1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()