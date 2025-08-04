from aiogram import Bot,Dispatcher
import asyncio
import os
from dotenv import load_dotenv
from app.rools.user import user
from app.rools.admin import admin
import redis.asyncio as aiored
from aiogram.fsm.storage.redis import RedisStorage
from app.DB.models import async_main

load_dotenv()
TOKEN = os.getenv("TOKEN")
async def main():
    redis = await aiored.from_url(f'redis://localhost:6379/0')
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis))
    dp.include_routers(admin,user)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await async_main()
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



