from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from flower_bot.keyboards.inline.admin_kb import (
    DataCallbackFactory,
    create_admin_start_kb,
    create_admin_stats_kb,
    create_back_button,
    create_crud_kb,
    create_crud_select_kb,
)
from flower_bot.repository.flower_point_repository import FlowerPointRepository
from flower_bot.repository.order_repository import OrderRepository
from flower_bot.repository.product_repository import ProductRepository
from flower_bot.repository.stock_repository import ProductFlowerPointRepository
from flower_bot.states import FSMAdminPanel

router = Router()



@router.callback_query(StateFilter(FSMAdminPanel.choose_action), F.data == 'stats')
async def process_stats_menu(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession) -> None:
    await callback.message.delete()
    
    await callback.message.answer(text='Выбери нужный вариант',
                                  reply_markup=create_admin_stats_kb()
                                  )
    await state.set_state(state=FSMAdminPanel.stats_menu)


@router.callback_query(StateFilter(FSMAdminPanel.stats_menu), F.data == 'stats_exact_point')
async def process_choose_type(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession) -> None:
    await callback.message.delete()
    data = await FlowerPointRepository(session=session).get_all_points()
    await callback.message.answer(text='Выбери нужную точку',
                                  reply_markup=create_crud_select_kb(data=data)
                                  )
    await state.set_state(state=FSMAdminPanel.choose_exact_point)


@router.callback_query(StateFilter(FSMAdminPanel.choose_exact_point), 
                       DataCallbackFactory.filter())
async def process_show_exact_point_stats(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession,
                                callback_data: DataCallbackFactory) -> None:
    await callback.message.delete()
    flower_remains = await FlowerPointRepository(session=session)\
        .get_remained_flowers_by_point(point_id=callback_data.entity_id)
    
    income = await FlowerPointRepository(session=session) \
        .get_income_by_point(point_id=callback_data.entity_id)
    if income is None:
        income = 0
    await callback.message.answer(text=f'Прибыль точки: {income}\n'
                                  f'Остаток цветов на точке: {flower_remains}',
                                  reply_markup=create_back_button()
                                  )
                                  
    await state.set_state(state=FSMAdminPanel.stats_menu)

@router.callback_query(StateFilter(FSMAdminPanel.stats_menu), F.data == 'stats_all_points')
async def process_all_points_stats(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession) -> None:
    
    await callback.message.delete()
    whole_income = await OrderRepository(session=session).get_income_from_all_points()
    all_remains = await ProductFlowerPointRepository(session=session)\
        .get_remained_flowers_all_points()
    await callback.message.answer(text=f'Прибыль по всем точкам: {whole_income}\n'
                                  f'Остаток цветов по всем точкам {all_remains}',
                                  reply_markup=create_back_button()
                                  )
    await state.set_state(FSMAdminPanel.end_state)
    

@router.callback_query(StateFilter(FSMAdminPanel.choose_action), F.data == 'manage_menu')
async def process_manage_button(callback: CallbackQuery,
                                state: FSMContext,
                                session: AsyncSession) -> None:
    await callback.message.delete()
    data = await FlowerPointRepository(session=session).get_all_points()
    await callback.message.answer(text='Вот список всех цветочных точек:',
                                  reply_markup=create_crud_select_kb(data=data)
                                  )
    await state.set_state(state=FSMAdminPanel.choose_point_to_crud)
    

@router.callback_query(StateFilter(FSMAdminPanel.choose_point_to_crud), 
                       DataCallbackFactory.filter())
async def process_choose_exact_point(callback: CallbackQuery,
                                state: FSMContext,
                                callback_data: DataCallbackFactory,
                                session: AsyncSession) -> None:
    await callback.message.delete()
    await state.update_data(point_id=callback_data.entity_id)
    await callback.message.answer(text='Выбери нужное действие',
                                  reply_markup=create_crud_kb()
                                  )
    await state.set_state(state=FSMAdminPanel.choose_crud_operation)


@router.callback_query(StateFilter(FSMAdminPanel.choose_crud_operation), F.data == 'update_stock')
async def process_update_stock_button(callback: CallbackQuery,
                                      session: AsyncSession,
                              state: FSMContext) -> None:
    cache_data = await state.get_data()
    flower_remains = await FlowerPointRepository(session=session)\
        .get_remained_flowers_by_point(point_id=cache_data['point_id'])
    await callback.message.answer(f"Текущий остаток цветов: {flower_remains}\n"
                                  "Введи числом новое количество цветов",
                                  )
    await state.set_state(FSMAdminPanel.input_flowers_number)


@router.callback_query(StateFilter(FSMAdminPanel.choose_point_to_crud), F.data == 'change_price')
async def process_update_price_button(callback: CallbackQuery,
                                      session: AsyncSession,
                              state: FSMContext) -> None:
    last_price = await ProductRepository(session=session).get_price_by_name(product_name='Белые тюльпаны')
    await callback.message.answer(f"Текущая цена за товар: {last_price}\n"
                                  "Введи числом новую цену",
                                  )
    await state.set_state(FSMAdminPanel.input_new_price)


@router.message(StateFilter(FSMAdminPanel.input_new_price), 
                F.text.func(lambda message: message.isdigit()))
async def process_new_price_button(message: Message,
                                      session: AsyncSession,
                                    state: FSMContext) -> None:
    await ProductRepository(session=session)\
        .update_price_by_name(product_name='Белые тюльпаны', new_price=int(message.text))
    await message.answer("Цена товара обновлена\n"
                        f"Новое количество - {message.text}",
                        reply_markup=create_back_button()
                        )
    await state.set_state(FSMAdminPanel.end_state)


@router.message(StateFilter(FSMAdminPanel.input_flowers_number), 
                F.text.func(lambda message: message.isdigit()))
async def process_create_new_point_button(message: Message,
                                      session: AsyncSession,
                              state: FSMContext) -> None:
    await message.delete()
    cache_data = await state.get_data()
    await ProductFlowerPointRepository(session=session)\
        .update_stock(point_id=cache_data['point_id'], new_quantity=int(message.text),
                      product_id=1)
    await message.answer(f"Кол-во цветов на точке обновлено.\n"
                                  f"Новое количество - {message.text}",
                                  reply_markup=create_back_button())
    await state.set_state(FSMAdminPanel.end_state)


@router.callback_query(StateFilter(FSMAdminPanel), F.data == 'back')
async def process_back_button(callback: CallbackQuery,
                              state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Вы перешли в начало меню.\nВыбери нужное действие",
                                  reply_markup=create_admin_start_kb())
    await state.set_state(FSMAdminPanel.choose_action)



@router.callback_query(StateFilter(FSMAdminPanel), F.data == 'exit')
async def process_exit_button(callback: CallbackQuery,
                              state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Админ-панель закрыта')