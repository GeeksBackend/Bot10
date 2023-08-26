from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token='6437786366:AAHkjcIFPdb9_kIIplawWyPMvISgFEn6VWM')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer('Привет Geeks!')

@dp.message_handler(commands='go')
async def command_go(message:types.Message):
    await message.answer('Комманда go сработала!')

@dp.message_handler(text='Привет')
async def hello(message:types.Message):
    await message.answer('Привет, как дела?')

@dp.message_handler(commands='test')
async def testing(message:types.Message):
    await message.reply('message.reply выделяет текст и отвечает вот так')
    await message.answer_dice()
    await message.answer_location(40.51932802196798, 72.80303735391686)
    await message.answer_photo('https://static.tildacdn.com/tild3863-3635-4138-b133-613431396662/230124-237_2.jpg')
    with open('1.png', 'rb') as photo: #Отправляем фото с ноутбука, а не с интеренета
        await message.answer_photo(photo)
    await message.answer_contact('0772343206', 'Kurmanbek', 'Toktorov')
    with open('voice.m4a', 'rb') as voice:
        await message.answer_voice(voice)

executor.start_polling(dp)