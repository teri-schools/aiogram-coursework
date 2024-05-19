from aiogram.fsm.state import StatesGroup, State


class CreatePerson(StatesGroup):
    input_name = State()

class CreateKavun(StatesGroup):
    input_weight = State()