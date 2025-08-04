from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Чат с искусственным интелектом'),
    KeyboardButton(text='Обычный чат с ботом')
]],resize_keyboard=True,
    input_field_placeholder='Выберите пункт ниже'
    )
inline_main_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль',callback_data='profile'),
     InlineKeyboardButton(text='Настройки бота',callback_data='settings_bot')],
    [InlineKeyboardButton(text='Версия чата gpt',callback_data='vers_gpt')]
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ваше имя',callback_data='username_set')],
    [InlineKeyboardButton(text='Ваш id',callback_data='userid_set')]
])

inline_DBBir_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть дни рождения',callback_data='search_Bir')],
    [InlineKeyboardButton(text='Добавить день рождения',callback_data='insert_Bir')]
])

inline_Title = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть задачи',callback_data='search_title')],
    [InlineKeyboardButton(text='Добавить задачи',callback_data='insert_title')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад',callback_data='back_settings')]
])