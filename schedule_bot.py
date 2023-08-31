from aiogram import Bot, Dispatcher, types, executor
import aioschedule, requests, logging, asyncio
from config import token 

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет!")

async def send_spam():
    await bot.send_message(731982105, "SPAM FROM PYTHON")

async def scheduler():
    aioschedule.every(1).seconds.do(send_spam)
    while True:
        await aioschedule.run_pending()

async def on_statup(parameter):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_statup)