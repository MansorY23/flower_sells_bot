from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from flower_bot.keyboards import (
    AmountCallbackFactory,
    create_confirm_keyboard,
    create_number_keyboard,
    create_payment_keyboard,
    create_sale_keyboard,
)
from flower_bot.repository import (
    FlowerPointRepository,
    OrderRepository,
    ProductFlowerPointRepository,
    ProductRepository,
    UserRepository,
)
from flower_bot.states import FSMSell

router = Router()


@router.message(StateFilter(default_state), F.text == 'Добавить продажу')
async def process_start_button(message: Message,
                               state: FSMContext,
                               session: AsyncSession) -> None:

    await message.answer(text='Жми кнопку чтобы добавить продажу',
                         reply_markup=create_sale_keyboard()
                         )
    await state.set_state(state=FSMSell.add_new_sale)


@router.callback_query(StateFilter(FSMSell.add_new_sale), F.data == 'add_sale')
async def process_flowers_sale(callback: CallbackQuery,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await callback.message.delete()

    await callback.message.answer(text='Выбери количество цветов из кнопки',
                         reply_markup=create_number_keyboard()
                         )
    await state.set_state(state=FSMSell.enter_flower_numbers)


@router.callback_query(StateFilter(FSMSell.enter_flower_numbers), F.data == 'entry_manual')
async def process_custom_input(callback: CallbackQuery,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await callback.message.delete()

    await callback.message.answer(text='Введи количество цветов одним числом')
    await state.set_state(state=FSMSell.enter_custom_flower_numbers)


@router.message(StateFilter(FSMSell.enter_custom_flower_numbers),
                 F.text.func(lambda message: message.isdigit()))
async def process_custom_input(message: Message,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await state.update_data(amount=int(message.text))

    await message.answer(text=f'Количество цветов: {message.text} \n'
                                        'Теперь выбери тип платежа',
                         reply_markup=create_payment_keyboard()
                         )
    await state.set_state(state=FSMSell.choose_payment_type)


@router.callback_query(StateFilter(FSMSell.enter_flower_numbers),
                        AmountCallbackFactory.filter())
async def process_number_buttons(callback: CallbackQuery,
                               state: FSMContext,
                               callback_data: AmountCallbackFactory,
                            session: AsyncSession) -> None:
    await callback.message.delete()
    await state.update_data(amount=callback_data.amount)
    await callback.message.answer(text=f'Количество цветов: {callback_data.amount} \n'
                                        'Теперь выбери тип платежа',
                         reply_markup=create_payment_keyboard()
                         )
    await state.set_state(state=FSMSell.choose_payment_type)


@router.callback_query(StateFilter(FSMSell.choose_payment_type),
                        F.data.in_({'cash', 'transfer'}))
async def process_payment_type_buttons(callback: CallbackQuery,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await callback.message.delete()

    if callback.data == 'cash':
        payment_type_format = 'наличка'
    elif callback.data == 'transfer':
        payment_type_format = 'перевод'

    await state.update_data(payment_type=payment_type_format)
    cache_data = await state.get_data()


    await callback.message.answer(text=f'Продано {cache_data["amount"]} тюльпан(ов), '
                                  f'способ оплаты - {payment_type_format}\n\n'
                                  'Если всё верно, нажми для подтверждения продажи',
                         reply_markup=create_confirm_keyboard()
                         )
    await state.set_state(state=FSMSell.sale_confirmation)


@router.callback_query(StateFilter(FSMSell.sale_confirmation), F.data == 'confirm')
async def process_confirm_button(callback: CallbackQuery,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await callback.message.delete()
    cache_data = await state.get_data()
    point_id = await UserRepository(session=session) \
        .get_flower_point_by_user(telegram_id=callback.from_user.id)
    price = await ProductRepository(session=session) \
        .get_price_by_name(product_name='Белые тюльпаны')
    await OrderRepository(session=session)\
        .create_new_order(amount=cache_data['amount'], order_sum=price*cache_data['amount'],
                          point_id=point_id, product_id=None)
    flowers_amount = await FlowerPointRepository(session=session) \
        .get_remained_flowers_by_point(point_id=point_id)
    
    flowers_remains: int = flowers_amount - cache_data['amount']
    await ProductFlowerPointRepository(session=session)\
        .update_stock(point_id=point_id, product_id=1, new_quantity=flowers_remains)
    
    income = await FlowerPointRepository(session=session) \
        .get_income_by_point(point_id=point_id)

    await callback.message.answer(text='Продажа подтверждена.\n'
                         f'Цветов осталось: {flowers_remains}\n'
                         f'Текущий доход: {income} \n'
                         f'Добавить ещё продажу?',
                         reply_markup=create_sale_keyboard()
                         )
    await state.set_state(state=FSMSell.add_new_sale)


@router.callback_query(StateFilter(FSMSell), F.data == 'cancel')
async def process_cancel(callback: CallbackQuery,
                               state: FSMContext,
                               session: AsyncSession) -> None:
    await callback.message.delete()
    await state.clear()

    await callback.message.answer(text='Ты отменил продажу\n'
                                        'Добавить новую?',
                                        reply_markup=create_sale_keyboard())
    await state.set_state(state=FSMSell.add_new_sale)
