from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Filter,Command
from aiogram.fsm.context import FSMContext
from app.states import State
from aiogram.enums import ChatAction
import asyncio
from app.DB.requests import get_users
from app.DB.requests import set_user
from app.keyboards import main
admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [1986006290]

@admin.message(Admin(),Command('start'))
async def start_admin(message:Message):
    await set_user(message.from_user.id)
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(1)
    await message.answer('Приветствую админ👋\n'
                   'Чтобы посмотреть список доступных команд введи <b>/help</b>',parse_mode='HTML',reply_markup=main)

@admin.message(Admin(),Command('help'))
async def admin_help(message:Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(1)
    await message.answer('Список команд⬇️\n'
                   '<b>/newsletter</b> - позволяет делать рассылку\n'
                   '<b>/database</b> - позволяет работать с базами данных',parse_mode='HTML')




@admin.message(Admin(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(1)
    await message.answer('📨Введите сообщение для рассылки')
    await state.set_state(State.message)


@admin.message(State.message)
async def newslet_mes(message: Message, state: FSMContext):
    await state.clear()
    users = await get_users()
    success = 0
    failed = 0

    await message.answer('Рассылка начата...')

    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user.tg_id}: {e}")
            failed += 1


    await message.answer(
        f'Рассылка завершена\n'
        f'Успешно: {success}\n'
        f'Не удалось: {failed}'
    )