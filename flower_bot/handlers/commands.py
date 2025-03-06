from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state

from flower_bot.filters import IsAdminFilter
from flower_bot.keyboards import create_admin_start_kb, create_user_reply_kb
from flower_bot.states import FSMAdminPanel, FSMSell

router = Router()


@router.message(Command('start'), StateFilter(any_state))
async def start_handler(message: types.Message,
                        state: FSMContext) -> None:
    await state.clear()
    if message.from_user is None:
        return
    await message.answer(f"Привет, {message.from_user.full_name}\n"
                         f"Это система учёта цветов.\n"
                         "Снизу две кнопки: добавить продажу и статистика\n\n"
                         "Статистика выведет количество оставшихся цветов и прибыль\n\n"
                         f"Твой id: {message.from_user.id}",
                         reply_markup=create_user_reply_kb()
                         )


@router.message(Command('help'), StateFilter(any_state))
async def help_handler(message: types.Message) -> None:
    if message.from_user is None:
        return
    await message.answer('Я тебе помогу.\n'
                         'Есть такие команды: /start, /cancel\n'
                         '/start - начать снова\n'
                         '/cancel - сбросить все действия ')


@router.message(Command('cancel'), StateFilter(any_state))
async def help_handler(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    await state.clear()
    await message.answer('Вы сбросили все действия и состояния.')


@router.message(Command('admin'), IsAdminFilter())
async def admin_panel_command(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Выбери нужное действие", reply_markup=create_admin_start_kb())
    await state.set_state(FSMAdminPanel.choose_action)


