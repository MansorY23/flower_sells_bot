from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DataCallbackFactory(CallbackData, prefix='flower_point'):
    entity_id: int


def create_admin_start_kb() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    buttons.append(InlineKeyboardButton(text='Cтатистика', callback_data='stats'))
    buttons.append(InlineKeyboardButton(text='Управление', callback_data='manage_menu'))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='Выйти', callback_data='exit'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_admin_stats_kb() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    buttons.append(InlineKeyboardButton(text='По всем точкам', callback_data='stats_all_points'))
    buttons.append(InlineKeyboardButton(text='Выбрать точку', callback_data='stats_exact_point'))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='Выйти', callback_data='exit'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_crud_select_kb(data: list) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    for flower_point in data:
        buttons.append(InlineKeyboardButton(
            text=flower_point.address,
            callback_data=DataCallbackFactory(entity_id=int(flower_point.id)).pack())
        )
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='Создать точку', callback_data='create_point'),
                   InlineKeyboardButton(text='Изменить цену', callback_data='change_price'))
    kb_builder.row(InlineKeyboardButton(text='В начало', callback_data='back'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_crud_kb() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    buttons.append(InlineKeyboardButton(text='Обновить кол-во ', callback_data='update_stock'))
    buttons.append(InlineKeyboardButton(text='Удалить точку', callback_data='delete_point'))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=2)
    kb_builder.row(InlineKeyboardButton(text='В начало', callback_data='back'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_back_button() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок

    kb_builder.row(InlineKeyboardButton(text='В начало',
                                        callback_data='back'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()