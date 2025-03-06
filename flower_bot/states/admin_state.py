from aiogram.fsm.state import State, StatesGroup


class FSMAdminPanel(StatesGroup):
    start_menu = State()
    choose_action = State()
    stats_menu = State()
    crud_menu = State()
    end_state = State()
    choose_exact_point = State()
    choose_point_to_crud = State()
    choose_crud_operation = State()
    input_flowers_number = State()
    input_new_price = State()
    create_new_point = State()