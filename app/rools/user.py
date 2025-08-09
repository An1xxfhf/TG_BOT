from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
import asyncio
import app.keyboards as kb
from app.states import State

from app.DB.requests import set_user,set_bir,get_birthdays,set_title,get_title
import aiohttp
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
user = Router()

API_Weather = os.getenv('API_WEATHER')
commands = ['start','help','weather','settings','birthday','title']

@user.message(Command('start'))
async def start(message: Message):
    await set_user(message.from_user.id)
    await message.bot.send_chat_action(chat_id=message.from_user.id,action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer(f"Привет, {message.from_user.first_name}👋\n"
                          f"Если хотите узнать, что может этот бот введите <b>/help</b>",parse_mode='HTML',reply_markup=kb.main)

@user.message(Command('help'))
async def help(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer(
        "<b>Вот список команд⬇️</b>\n"
        "<b>/weather</b> - узнать погоду в городе\n"
        "<b>/birthday</b> - управление днями рождения\n"
        "<b>/title</b> - список дел\n"
        "<b>/settings</b> - настройки профиля",
        parse_mode="HTML")

@user.message(Command('weather'))
async def weather(message: Message,state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer('Введите название города: ')
    await state.set_state(State.location_weather)


@user.message(State.location_weather)
async def get_weather(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.FIND_LOCATION
    )
    await asyncio.sleep(1)

    city = message.text.strip().lower()

    weather_translation = {
        "clear sky": "☀ ясно",
        "few clouds": "🌤 небольшая облачность",
        "scattered clouds": "⛅ облачно с прояснениями",
        "broken clouds": "☁ пасмурно",
        "overcast clouds": "☁ сплошная облачность",
        "mist": "🌫 дымка",
        "fog": "🌁 туман",
        "light rain": "🌦 небольшой дождь",
        "moderate rain": "🌧 умеренный дождь",
        "heavy rain": "⛈ сильный дождь",
        "light snow": "❄ небольшой снег",
        "moderate snow": "❄ умеренный снег",
        "heavy snow": "❄ сильный снег",
        "thunderstorm": "⚡ гроза",
        "haze": "🌫 мгла",
        "smoke": "💨 смог",
        "dust": "💨 пыль",
        "sand": "💨 песчаная буря",
        "squalls": "💨 шквалы",
        "tornado": "🌪 торнадо"
    }
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Weather}&units=metric&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                # Проверяем статус ответа
                if response.status != 200:
                    try:
                        error_data = await response.json()
                        error_msg = error_data.get('message', 'Unknown error')
                        await message.answer(f"❌ Ошибка API: {error_msg} (код {response.status})")
                    except:
                        await message.answer(f"❌ Ошибка сервера: HTTP {response.status}")
                    return

                data = await response.json()

                # Проверка наличия необходимых данных
                if 'main' not in data or 'weather' not in data:
                    await message.answer("⚠️ Неполные данные от сервера погоды")
                    return

        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]

        temp = main["temp"]
        feels_like = main["feels_like"]
        weather_desc = weather_translation.get(
            weather["description"].lower(),
            weather["description"]
        )

        reply_text = (
            f"🌍 <b>Погода в {city.capitalize()}</b>\n\n"
            f"🌡 <b>Температура:</b> {temp}°C (ощущается как {feels_like}°C)\n"
            f"☁ <b>Состояние:</b> {weather_desc.capitalize()}\n"
            f"💧 <b>Влажность:</b> {main['humidity']}%\n"
            f"📊 <b>Давление:</b> {main['pressure']} hPa\n"
            f"🌬 <b>Ветер:</b> {wind['speed']} м/с"
        )

        if temp <= 0:
            reply_text += "\n\n❄️ Очень холодно! Теплая зимняя одежда обязательна."
        elif 0 < temp <= 10:
            reply_text += "\n\n🧥 Довольно прохладно. Наденьте теплую куртку."
        elif 10 < temp <= 18:
            reply_text += "\n\n🍂 Прохладно. Легкая куртка или теплый свитер."
        elif 18 < temp <= 25:
            reply_text += "\n\n👕 Комфортная температура. Легкая одежда."
        else:
            reply_text += "\n\n🔥 Жарко! Легкая летняя одежда."

        await message.answer(reply_text, parse_mode="HTML")


    except asyncio.TimeoutError:

        await message.answer("⌛ Сервер погоды не ответил вовремя. Попробуйте позже.")

    except aiohttp.ClientError as e:

        await message.answer(f"🌐 Ошибка сети: {str(e)}")

    except Exception as e:
        await message.answer("⚠️ Внутренняя ошибка при обработке запроса")
    finally:
        await state.clear()


@user.message(Command('birthday'))
async def Birthday(message:Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer('Выберите пункт:',reply_markup=kb.inline_DBBir_user)

@user.callback_query(F.data=="search_Bir")
async def handle_show_birthdays(callback: CallbackQuery):
    owner_id = callback.from_user.id
    birthdays = await get_birthdays(owner_id)

    if not birthdays:
        await callback.answer("Вы еще не добавили дни рождения", show_alert=True)
        return

    response = "Ваши дни рождения:\n"
    for bd in birthdays:
        response += f"- {bd['name_user']}: {bd['birth_date'].strftime('%d.%m.%Y')}\n"

    await callback.message.answer(response)
    await callback.answer()

@user.callback_query(F.data=="insert_Bir")
async def set_birh(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer('Введите имя в таком формате:\n\n'
                                  'Имя: Иван')
    await state.set_state(State.add_name)
    await callback.answer('')

@user.message(State.add_name)
async def reg_name(message:Message,state:FSMContext):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Имя должно содержать только буквы. Попробуйте еще раз.")
        return
    await state.update_data(name=name)
    await message.answer('Отлично,теперь введите дату рождения в таком формате:\n\n'
                         'ДД/ММ/ГГГГ (например: 16/12/2007)')
    await state.set_state(State.add_date)

@user.message(State.add_date)
async def ref_date(message:Message,state:FSMContext):
    try:
        date_str = message.text.strip()
        birth_date = datetime.strptime(date_str, "%d/%m/%Y").date()

        if birth_date > datetime.now().date():
            await message.answer("Дата не может быть в будущем. Попробуйте еще раз.")
            return

        data = await state.get_data()
        name = data['name']

        await set_bir(
            name=name,
            birth_date=birth_date,
            owner_id=message.from_user.id,
        )

        await message.answer(
            f"✅ День рождения для {name} ({birth_date.strftime('%d.%m.%Y')}) сохранен!"
        )
        await state.clear()

    except ValueError:
        await message.answer(
            "Неправильный формат даты. Используйте ДД/ММ/ГГГГ (например: 16/12/2007)\n"
            "Попробуйте еще раз:"
        )


@user.message(Command('settings'))
async def user_set(message:Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer('Выберите пункт',reply_markup=kb.inline_main_user)

@user.message(Command('title'))
async def title(message:Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer('Выберите пункт:', reply_markup=kb.inline_Title)

@user.callback_query(F.data == 'insert_title')
async def insert_title(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text('Введите свою задачу')
    await state.set_state(State.add_title)
    await callback.answer('')

@user.message(State.add_title)
async def add_title(message:Message,state:FSMContext):
    user_title=message.text.strip()
    await state.update_data(user_title=user_title)
    await set_title(
        title_user=user_title,
        owner_id=message.chat.id
    )
    await message.answer('Поздравляю, задача успешно установлена')
    await state.clear()

@user.callback_query(F.data == 'search_title')
async def search_title(callback:CallbackQuery):
    owner_id = callback.from_user.id
    titile = await get_title(owner_id=owner_id)

    if not titile:
        await callback.answer("Вы еще не добавили задачи",show_alert=True)
        return
    response = "Ваши задачи:\n"
    for bd in titile:
        response += f"- {bd['title_user']}\n"

    await callback.message.answer(response)
    await callback.answer()








@user.callback_query(F.data == 'profile')
async def profile(callback:CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите подпункт',reply_markup=kb.profile)

@user.callback_query(F.data == 'username_set')
async def username_set(callback:CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'Ваше имя: {callback.from_user.first_name}',reply_markup=kb.back)

@user.callback_query(F.data == 'userid_set')
async def userid_set(callback:CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'Ваш id: {callback.from_user.id}', reply_markup=kb.back)

@user.callback_query(F.data == 'back_settings')
async def back_settings(callback:CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите пункт',reply_markup=kb.inline_main_user)


@user.message(~F.text.startswith('/'))
async def wrong_command(message: Message):
    await message.answer(
        'Пожалуйста, выберите команду из списка!\n'
        'Введите /help для просмотра доступных команд'
    )



