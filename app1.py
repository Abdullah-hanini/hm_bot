"""#!/usr/bin/python3.10
from JokerAPI import JokerMethod, Number

# Joker Initiatior
JokerInstance = JokerMethod()

# Set API Key
JokerInstance.api_key = "mA91SG0XdS6ZUX2SEivdhD107AopdAfZ"

# Dial '+111111111' from '+111111111'.
sid: str | None = JokerInstance.dial(dial_to = Number("+19402773253"), dial_from = Number("16233884333")) 


call_sid: str | None = JokerInstance.dial(dial_to = Number("+111111111"), dial_from = Number("111111111")) 

# Play audio into the live channel
JokerInstance.play_text(call_sid, "hello world")"""
"""from aiogram import Bot, Dispatcher, types

import requests
phone_number = "19402773253"
name = "abd"

# The URL of the route in your local Flask app
url = f"https://9d67-178-77-185-147.ngrok-free.app/makecall/{phone_number}/{name}"

# Making the POST request
response = requests.post(url)
"""
import requests
import logging
from aiogram import Bot, Dispatcher, types
import JokerAPI
import aiohttp
import json
# Joker Initiatior

# Set API Key
API_TOKEN = '6409753184:AAGdJ3GBWBM2TkeFaJ-8nLB4qsjQakVy4AQ'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm a bot to make calls via Joker API!\nUse /call to make a call.")

@dp.message_handler(commands=['call'])
async def make_call(message: types.Message):
    chat_id = message.chat.id
    msg = message.text.split()

    if len(msg) == 3:
        number = str(msg[1])
        name = msg[2]

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',

        }

        data = {
            'to': '+'+number,
            'from': '+16233884333',
            'callback_url': 'https://settled-perch-nationally.ngrok-free.app/makecall/'+str(chat_id)+"/"+name,
            'type': 'api',
            'amd_enabled': True,  
            'record_enabled': True  
        }

        response = requests.post(
            'https://api.apivalley.su/api/v1/calls/create-call',
            headers=headers,
            json=data,  
            auth=('9acf0625-38e6-4a04-8f31-3163145b121f', 'Q8Drtr3qZfdNbHtSdwoCG5yME0s8Vy5N4Vt7qEtfKXWjhaptYQ2giI0Dof8faM60'),
        )
        if response.status_code == 200:
            response_data = response.json()  # Parse JSON response content
            if 'data' in response_data and 'call_id' in response_data['data']:
                print(response_data['data']['call_id'])
            else:
                print("The 'data' or 'call_id' key is not in the JSON response.")
        else:
            print("Failed to create call. Status code:", response.status_code)
            print("Response content:", response.text)
    await message.reply(name)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    # Here you can make a POST request to your server
    server_url = "https://settled-perch-nationally.ngrok-free.app/otp"
    data = json.loads(callback_query.data)

    async with aiohttp.ClientSession() as session:
        async with session.post(server_url, json=data) as response:
            response_data = await response.text()

    # You can also send an answer to the callback query
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    from aiogram import executor

    # setup logging
    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dp, skip_updates=True)
