#from aiogram import types, Dispatcher
from create_bot import dp
import json, string
from vk_maria import types
from keyboards import kb_client_main_menu
#@dp.message_handler()
def echo_send_mat(message : types.Message):
	if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.message.text.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set():
		message.answer(message = 'Общайтесь пожалуйста без мата')
	else:		
		message.answer(message = 'Не понимаю о чем вы. Используйте клавиатуру', keyboard = kb_client_main_menu)

def register_handlers_others(dp : dp):
	dp.register_message_handler(echo_send_mat)