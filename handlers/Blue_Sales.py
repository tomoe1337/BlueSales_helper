from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from bluesalespy import BlueSales
from config import VK_API_TOKEN
import vk_api


class authorization_state(StatesGroup):
	loginPass = State()
	isAutorizare = State()
	ask_cust_id = State()



def is_number(_str):
	try:
		int(_str)
		return True
	except ValueError:
		return False

async def ask_auth_data(message:types.Message, state = FSMContext):
	await authorization_state.loginPass.set()
	await bot.send_message(message.from_user.id,"Привет!Что бы воспользоваться ботом, введи данные от своей бс-ки одним сообщением\nПример:\n\noguzok99@gmail.com\n12345")


async def try_authorization(message:types.Message, state = FSMContext):
	if message.text != '/start':
		data = (message.text).split('\n')
		login = str(data[0])
		password = str(data[1])
		try:
			blue_sales = BlueSales(login, password)
			blue_sales.users.get()
			async with state.proxy() as data:
				data['loginPass'] = (login,password)

			await authorization_state.next()
			await bot.send_message(message.from_user.id,'Вы успешно авторизировались.Отправьте ссылку на лида в этот чат, чтобы узнать о нем')

		except Exception as e:
			print(e)
			await bot.send_message(message.from_user.id,f'Неправильный логин или пароль(\nПопробуйте еще раз\n')
	else:
		await ask_auth_data(message,state)

async def get_customer(message:types.Message, state = FSMContext):
	if message.text.lower() != "выйти":
		async with state.proxy() as data:
			login,password = data['loginPass']

		blue_sales = BlueSales(login, password)

		customers_vk_id = ((message.text).split('/')[-1])
		if is_number(customers_vk_id[2:]) == False:
			vk_session = vk_api.VkApi(token = VK_API_TOKEN)
			vk = vk_session.get_api()

			try:
				customers_vk_id = str(vk.users.get(user_ids = customers_vk_id)[0]['id'])
			except:
				return await bot.send_message(message.from_user.id,'Такой страницы в ВК нет, пропробуйте еще раз\nЕсли хотите выйти из вашего аккаунта бс, напишите "Выход"')


		response = blue_sales.customers.get(vk_ids =[customers_vk_id.strip('id')])

		if len(response.customers)<1:
			text = 'Данного клиента в вашей бс-ке нет\nЕсли хотите выйти из вашего аккаунта бс, напишите "Выход"'
		else:
			text = f"Имя: {response.customers[0]['fullName']}\nСтатус: {response.customers[0]['crmStatus']['name']}\nДата последнего контакта:{response.customers[0]['lastContactDate']}\nМенеджер: {response.customers[0]['manager']['fullName']}"

		await bot.send_message(message.from_user.id,text)
	else:
		await bot.send_message(message.from_user.id,"Вы вышли из аккаунта, для повторного входа введите /start")
		await state.finish()



def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(ask_auth_data,commands=['start','help'])
	dp.register_message_handler(try_authorization,state=authorization_state.loginPass)
	dp.register_message_handler(get_customer,state=authorization_state.isAutorizare)
