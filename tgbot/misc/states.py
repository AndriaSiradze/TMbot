from aiogram.fsm.state import StatesGroup, State


class SelectStudies(StatesGroup):
    select_city = State()
    select_date = State()


class QuestionAnswer(StatesGroup):
    name = State()
    age = State()
    city = State()
    university = State()
    phone = State()
