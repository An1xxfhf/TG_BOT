from aiogram.fsm.state import StatesGroup,State
class State(StatesGroup):
    location_weather = State()
    AIchat = State()
    wait = State()
    message = State()
    add_name = State()
    add_date = State()
    add_title = State()

