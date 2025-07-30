from aiogram.fsm.state import State, StatesGroup as AiogramStatesGroup


class States(AiogramStatesGroup):
    product = State()
    category = State()
    variant = State()
    flavor = State()
    rating_arina = State()
    comment_arina = State()
    rating_andrew = State()
    comment_andrew = State()
