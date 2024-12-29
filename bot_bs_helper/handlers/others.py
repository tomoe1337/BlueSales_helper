from aiogram import types, Dispatcher
from create_bot import dp
import json, string


async def echo_send_mat(message : types.Message):
	if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set():
		await message.answer('Общайтесь пожалуйста без мата')
	else:		
		await message.answer('Не понимаю о чем вы. Попробуйте ввести /start')

def register_handlers_others(dp : dp):
	dp.register_message_handler(echo_send_mat)