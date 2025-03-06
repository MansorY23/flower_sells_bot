from aiogram.fsm.state import State, StatesGroup


class FSMSell(StatesGroup):
    start_work = State()
    add_new_sale = State()
    enter_flower_numbers = State()
    enter_custom_flower_numbers = State()
    choose_payment_type = State()
    sale_confirmation = State()
