from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token 
import os, time, logging, sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('check.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT,
    username VARCHAR(200),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    created VARCHAR(100)
);
""")
cursor.connection.commit()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO users VALUES ({message.from_user.id}, '{message.from_user.username}', '{message.from_user.first_name}', '{message.from_user.last_name}', '{time.ctime()}');") #не забываем в конце знак ;
        cursor.connection.commit()
    await message.answer(f"Привет, {message.from_user.full_name}!")

class MailingState(StatesGroup):
    text = State()

@dp.message_handler(commands='mailing')
async def send_mailing(message:types.Message):
    if message.from_user.id in [731982105, ]:
        await message.answer("Введите текст для рассылки:")
        await MailingState.text.set()
    else: 
        await message.answer("У вас нету доступа")

@dp.message_handler(state=MailingState.text)
async def send_mailing_text(message:types.Message, state:FSMContext):
    cursor.execute("SELECT id FROM users;")
    users_id = cursor.fetchall()
    # print(users_id)
    for user in users_id:
        await bot.send_message(user[0], message.text)
    await state.finish()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял введите /start")

executor.start_polling(dp, skip_updates=True)