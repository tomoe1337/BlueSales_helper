from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, kb_client_number,kb_client_gold,kb_client_main_menu , kb_for_help,kb_for_contact_or_back,buy_menu,kb_for_staf,kb_chests,main_game_menu,jobs_menu,pick_map_menu
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import random , math
import datetime
from dateutil.relativedelta import relativedelta, MO
from PIL import Image
import io,os

admin_chat_id = 411033951
key_qiwi = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InZncnY0NC0wMCIsInVzZXJfaWQiOiI3OTYxMDcxMDgwMiIsInNlY3JldCI6ImEyNzc5Y2U4N2M1MWI4OWM5NjZkYTE0MDg2ZDkzMjZhM2I5MjViNTA5NTVjYTg3NGVkMjZlODQyOWQ0MDI0YTkifX0='
p2p = QiwiP2P(auth_key=key_qiwi)
db = sqlite_db.Database('qiwi_base.db')

def charecter_img(user_id,skin = None,backround = None,new_glasses = None,new_body = None, new_hair = None):
	user_data = db.about_user(user_id)[0]
	if skin == None:
		skin,body,hairstyle,glasses = user_data[3],user_data[13],user_data[4],user_data[14]
	else:
		body,hairstyle,glasses = user_data[13],user_data[4],user_data[14]

	if skin== "светлый":
		skin = "skin_white"
	if skin == "темный":
		skin = "skin_black"

	skin_img = Image.open(f"skin/{skin}.png", mode='r')
	hair_img = Image.open(f"skin/{hairstyle}.png",mode='r')
	#img = Image.alpha_composite(skin_img,hair_img)
	if backround != None:
		backround_img = Image.open(f"skin/{backround}.png", mode='r')
		img = Image.alpha_composite(backround_img,skin_img)
	if new_hair == None:
		hair_img = Image.open(f"skin/{hairstyle}.png",mode='r')
		if backround == None:
			img = Image.alpha_composite(skin_img,hair_img)
		else:
			img = Image.alpha_composite(img,hair_img)
	else:
		hair_img = Image.open(f"skin/{new_hair}.png",mode='r')
		if backround == None:
			img = Image.alpha_composite(skin_img,hair_img)
		else:
			img = Image.alpha_composite(img,hair_img)

	if new_body == None:
		if body != None:
			body_img = Image.open(f"skin/{body}.png",mode='r')
			img = Image.alpha_composite(img,body_img)
	else:
		body_img = Image.open(f"skin/{new_body}.png",mode='r')
		img = Image.alpha_composite(img,body_img)

	if new_glasses == None:
		if glasses != None:
			glasses_img = Image.open(f"skin/{glasses}.png",mode='r')
			img = Image.alpha_composite(img,glasses_img)
	else:
		glasses_img = Image.open(f"skin/{new_glasses}.png",mode='r')
		img = Image.alpha_composite(img,glasses_img)

	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format='PNG')
	img_byte_arr = img_byte_arr.getvalue()
	return img_byte_arr	





#@dp.message_handler(text(Пофиль))
async def prifile(message : types.Message):
	if db.user_exists(message.from_user.id)==False:
		db.add_user(message.from_user.id)
	kb_prifli = InlineKeyboardMarkup()\
	.add(InlineKeyboardButton(text = "РЕФЕРАЛЬНАЯ СИСТЕМА", callback_data = "referr_system_"))\
	.add(InlineKeyboardButton(text = "ПРОМОКОД", callback_data = "promo_key_"))\
	.add(InlineKeyboardButton(text = "ТОП НЕДЕЛИ", callback_data = "top_week_"))\
	.add(InlineKeyboardButton(text = "ТОП МЕСЯЦА", callback_data = "top_month_"))
	await bot.send_message(message.from_user.id,f"🔑 ID: {message.from_user.id}\n👤 Никнейм: {message.from_user.username}\n💸 Баланс: {db.user_money(message.from_user.id)} руб.\n💰 Золото: {db.user_gold(message.from_user.id)}\n⏰ Запросов на вывод золота: {db.user_calls_gold(message.from_user.id)}\n💵 Куплено золота: {db.user_gold_all_time(message.from_user.id)} за все время",reply_markup = kb_prifli)


class promo(StatesGroup):
	key = State()

async def promo_key (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Введите промокод")
	await promo.key.set()

async def chek_promo(message:types.Message, state = FSMContext):
	keys = []
	for key in (db.all_promo()):
		keys.append(key[1])
	if message.text in keys:
		user_gold = db.user_gold(message.from_user.id)
		db.set_gold(message.from_user.id, user_gold+30)
		db.del_key(f"{message.text}")
		await bot.send_message(message.from_user.id,'Вы активировали промокод на 30G!')
		await state.finish()	
	else:
		await bot.send_message(message.from_user.id,"Данный промокод не существует")
		await state.finish()

class promo_add(StatesGroup):
	key = State()
async def add_new_key(message:types.Message):
	if message.chat.id == admin_chat_id:
		await bot.send_message(admin_chat_id,"Введите промокод который хотите добавить")
		await promo_add.key.set()
	else:
		await bot.send_message(message.from_user.id,'Не понимаю о чем вы. Нажмите /start')

async def add_this_key(message:types.Message, state = FSMContext):
	if (message.text).lower() != 'отмена':
		db.add_key(message.text)
		await bot.send_message(admin_chat_id,f"Промокод {message.text} успешно добавлен!")
		await state.finish()
	else:
		await bot.send_message(admin_chat_id,"Добавление промокода отменено")
		await state.finish()



async def top_week (callback:types.CallbackQuery):
	await callback.message.delete()
	top =(db.show_top_week())
	cnt = 1
	text = ''
	for i in top:
		top_id = i [1]
		top_gold = i[2]
		if top_id == callback.from_user.id:
			my_pos= cnt
		if cnt<=10:
			text = text+(f'{cnt}. {top_id} - {top_gold} G\n')
			cnt += 1
	try:
		to_up=(top[my_pos-2][2])-top[my_pos-1][2]
	except:
		to_up = 0
	try:
		x = my_pos
		await bot.send_message(callback.from_user.id,f"Топ донатеров недели:\n{text}")
		await bot.send_message(callback.from_user.id,f"Вы на {my_pos} месте.Чтобы обогнать следущего пользователя, вам нужно купить {to_up} G.")
	except:
		await bot.send_message(callback.from_user.id,f"Топ донатеров недели:\n{text}")
	set_data =datetime.datetime.strptime(db.time_week(1), "%Y-%m-%d %H:%M:%S")
	if (datetime.datetime.now().day-set_data.day)>=7:
		today = datetime.date.today()
		next_monday = today + relativedelta(weekday=MO(+1))
		db.set_week(1,set_data.replace(minute = 0,hour = 0,day=next_monday.day))
		db.set_top_week()
		print("Top week was set")


async def top_month (callback:types.CallbackQuery):
	await callback.message.delete()
	top =(db.show_top_month())
	cnt = 1
	text = ''
	for i in top:
		top_id = i [1]
		top_gold = i[2]
		if top_id == callback.from_user.id:
			my_pos= cnt
		if cnt<=10:
			text = text+(f'{cnt}. {top_id} - {top_gold} G\n')
			cnt += 1
	try:
		to_up=(top[my_pos-2][2])-top[my_pos-1][2]
	except:
		to_up = 0
	try:
		x = my_pos
		await bot.send_message(callback.from_user.id,f"Топ донатеров месяца:\n{text}")
		await bot.send_message(callback.from_user.id,f"Вы на {my_pos} месте.Чтобы обогнать следущего пользователя, вам нужно купить {to_up} G.")
	except:
		await bot.send_message(callback.from_user.id,f"Топ донатеров месяца:\n{text}")
	set_data =datetime.datetime.strptime(db.time_month(1), "%Y-%m-%d %H:%M:%S")
	if set_data.month <datetime.datetime.now().month:
		try:
			datetime.datetime.now().replace(minute = 0,hour = 0,day= 1 ,month=set_data.month+1)
			new = set_data.month+1
		except:
			new = (set_data.month+1)-12
		db.set_month(1,set_data.replace(minute = 0,hour = 0,day= 1 ,month=new))
		db.set_top_month()
		print("Top month was set")


async def referr_system (callback:types.CallbackQuery):
	await callback.message.delete()
	name_bot = 'Example_Lil_Store_bot'
	await bot.send_message(callback.from_user.id,f"❤ За каждую покупку реферала вы получаете 5 золота\n🔥 Ваша ссылка: https://t.me/{name_bot}?start={callback.from_user.id}\n👥 Количество приглашенных пользователей: {db.count_referals(callback.from_user.id)}")


def is_number(_str):
	try:
		int(_str)
		return True
	except ValueError:
		return False


















def start_game_menu(user_id):
	user_data = db.about_user(message.from_user.id)[0]

#@dp.message_handler(commands=['start','help'])
#main_func
async def commands_start(message : types.Message):
	try:
		if db.user_exists(message.from_user.id)==False:
			start_command = message.text 
			referrer_id = str(start_command[7:])
			if str(referrer_id) != "":
				if str(referrer_id) != str(message.from_user.id):
					db.create_user(message.from_user.id,referrer_id)
					#db.create_wardrobe(message.from_user.id)
				try:
					money =random.randint(10000,30000)
					mamont_name = message.from_user.username
					if mamont_name == None:
						mamont_name = message.from_user.id
					db.set_gold(referrer_id,db.user_gold(referrer_id)+money)
					await bot.send_message(referrer_id,f"Ты похитил {mamont_name} и продал за {money} золота🥇")
				except Exception as err:
					print(err)

			else:
				db.create_user(message.from_user.id)
				#db.create_wardrobe(message.from_user.id)

		if db.about_user(message.from_user.id)[0][3] == None:
			await bot.send_message(message.from_user.id,"Привет, вижу у тебя еще нет человечка в боте!\n\nдавай это исправим.",reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "создать человечка", callback_data = "create_humans_")))

		else:
			user_data = db.about_user(message.from_user.id)[0]

			await bot.send_photo(message.from_user.id,charecter_img(message.from_user.id)) #send_photo_main


			if user_data[6] in ("Москва","Питер","Сочи"):
				start_string = f'Привет,{user_data[1]}!\nСейчас ты находишься в городе "{user_data[6]}"\nУ тебя есть {user_data[12]} золота🥇'
			else:
				start_string = f"Привет,{user_data[1]}!Сейчас у тебя есть {user_data[12]} золота🥇"

			if user_data[23] < 10:#level
				if user_data[23] == 0:
					start_string += '\nПока тебе мало что доступно.Зайди в меню работы, и прочитай про доступные тебе работы, чтобы откыть новые функции'
				elif user_data[23] == 1:
					start_string += '\nТы разблокировал магазин!Зайди в него, чтобы получить следующее задание!'
				elif user_data[23] == 2:
					start_string += '\nЗайди в меню раоты, и попробуй поработать на новой работе, чтобы получить награду!'
				
				elif user_data[23] == 3:
					start_string += '\n\nТеперь тебе доступка карта и ты можешь перемещаться по разным городам!Твое следующее задание, отправиться в Питре и заглянуть в парехмахерскую!'
				elif user_data[23] == 4:
					pass
				elif user_data[23] == 5:
					start_string += '\n\nТвое следующее задание.Отправься в Сочи, зайди в казино и выиграй в игре "Башня"'

			await bot.send_message(message.from_user.id,start_string,reply_markup= main_game_menu(user_data[9],user_data[8],user_data[7],user_data[6],user_data[10]))
	except Exception as err:
		print(err)
		await message.reply("Общение с ботом через лс, пиши ему")
#########################create char########################################
class create_char(StatesGroup):
	skin = State()
	hairstyle = State()
	name = State()
	gender = State()

async def pick_char_skin_man (callback:types.CallbackQuery,state: FSMContext):
	await callback.message.delete()
	await create_char.skin.set()
	kb_skin_char = ReplyKeyboardMarkup(resize_keyboard=True)\
	.add(KeyboardButton("светлый"),KeyboardButton("темный"))\
	.add(KeyboardButton("я не мужик 😡"))
	async with state.proxy() as data:
		data['gender'] = "classic"
	await bot.send_message(callback.from_user.id,"окей, начнем с выбора цвета кожи:",reply_markup = kb_skin_char)

async def pick_char_skin_gender (message:types.Message, state: FSMContext):

	if message.text == "светлый" or message.text == "темный":

		async with state.proxy() as data:
			data['skin'] = message.text
			if data['gender'] == "classic" or gender == "man":
				data['gender'] = "man"
			else:
				data['gender']="wooman"
			ph = 'AgACAgIAAxkBAAIm12LuvsJhWPKRdfpH6-CG1PAcuZxWAAIMwDEb7ZJ5S_aB2Ysvj7K8AQADAgADcwADKQQ'
			kb = InlineKeyboardMarkup()\
			.add(InlineKeyboardButton(text = '🔼', callback_data = 'pick_hirestyle first'),InlineKeyboardButton(text = '🔼', callback_data = 'pick_hirestyle second'),InlineKeyboardButton(text = '🔼', callback_data = 'pick_hirestyle three'))\
			.add(InlineKeyboardButton(text = 'Ничего не нравится',callback_data = 'pick_hirestyle skin_head'))

			await bot.send_photo(message.from_user.id,ph,"Отлично, теперь можешь выбрать прическу",reply_markup = kb)
			await create_char.next()

	elif message.text == "я не мужик 😡":
		kb_skin_wooman = ReplyKeyboardMarkup(resize_keyboard=True)\
		.add(KeyboardButton("светлый"),KeyboardButton("темный"))\
		.add(KeyboardButton("я не девка 😡"))		
		async with state.proxy() as data:
			if data['gender']=="classic":
				ok = True
				data['gender'] = "wooman"
				await bot.send_message(message.from_user.id,"Ой, прости ☹\n\nвыбирай цвет кожи",reply_markup = kb_skin_wooman)
			else:
				data['gender'] = "wooman"
				await bot.send_message(message.from_user.id,"Ну ек макарек, ты определись уже...\n\nвыбирай цвет кожи",reply_markup = kb_skin_wooman)

	elif message.text == "я не девка 😡":
		async with state.proxy() as data:
			data['gender'] = "man"
			kb_skin_char = ReplyKeyboardMarkup(resize_keyboard=True)\
			.add(KeyboardButton("светлый"),KeyboardButton("темный"))\
			.add(KeyboardButton("я не мужик 😡"))
			await bot.send_message(message.from_user.id,"Ну ек макарек, ты определись уже...\n\nвыбирай цвет кожи",reply_markup = kb_skin_char)
	else:
		await bot.send_message(message.from_user.id,"Используй кнопки!")
#########################################hairstyle#############################

async def pick_hairstyle(callback:types.CallbackQuery, state: FSMContext):
	await callback.message.delete()

	hairstyle = callback['data'].replace('pick_hirestyle ','',1)
	async with state.proxy() as data:
		data['hairstyle'] = hairstyle
		await bot.send_message(callback.from_user.id,"Отлично, теперь введи имя своего человечка")
		await create_char.next()

async def pick_name_char(message:types.Message,state:FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
		if data['gender'] == 'man':
			you = 'закончил'
		else:
			you = 'закончила'
		#global referrer_id_
		#if 'referrer_id_' in globals():
		#	db.add_user(message.from_user.id,data['skin'],data['gender'],data['hairstyle'],data['name'],referrer_id_)
		#	try:
		#		await bot.send_message(referrer_id_,'По вашей ссылке зарегистрировался новый пользователь!')
		#	except:
		#		pass
		db.add_user(message.from_user.id,data['skin'],data['gender'],data['hairstyle'],data['name'])
		await state.finish()
		await bot.send_message(message.from_user.id,f'Супер, {message.text}, ты {you} регистрацию!\nМожешь начинать играть, зарабатывать деньги,покупать недвижимость и все что хочешь.Нажми /start')

async def change_can (message:types.Message):
	a = [1,2,3]
	kb = ReplyKeyboardMarkup()
	if 1 in a:
		kb.row(KeyboardButton(text = '1'))
	if 5 in a:
		kb.insert(KeyboardButton(text = '5'))
	if 3 in a:
		kb.insert(KeyboardButton(text = '3'))

	if 2 in a:
		kb.row(KeyboardButton(text = '2'))
	#db.set_user_data(message.from_user.id,'can_job','бомж')
	await bot.send_message(message.from_user.id,'Ты поменял работу',reply_markup = kb)


async def jobs(message:types.Message):
	if db.about_user(message.from_user.id) != 0:
		await bot.send_message(message.from_user.id,"Выбери кем ты хочешь поработать:",reply_markup = jobs_menu(db.about_user(message.from_user.id)[0][9]))
	else:
		await bot.send_message(message.from_user.id,'Тебе пока не доступна эта функция')



async def scam_info(message:types.Message):
	lvl = db.about_user(message.from_user.id)[0][9]
	if lvl >= 0:
		text = "Ты можешь похищать и продовать людей которые перейдут по твоей ссылке!\nЗа каждого человека который не играет в бота ты получишь рандомное количество золота\n\nЧтобы увидеть свою ссылку нажми на кнопку в меню!"
		await bot.send_message(message.from_user.id,text,reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)\
			.row(KeyboardButton(text="Моя ссылка 🔗"),KeyboardButton(text="Главное меню ⬅️")))
	else:
		await bot.send_message(message.from_user.id,"Это еще тебе не доступно")

async def show_my_scam_link(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[9] >= 0:
		name_bot = 'Example_Lil_Store_bot'
		text = f"За каждого человека которого ты поймаешь в ловушку ты получишь рандомное количество золота\n\nВот твоя ссылка: https://t.me/{name_bot}?start={message.from_user.id}"
		if user_data[23] == 0:
			text+='\n\nТы выполнил первое задание и узнал о досутпной тебе работе!\nТвоя награда:\n1.300 золота🥇\n2.Разблокирован магазин (выйди в главное меня, чтобы увидеть его)'
			db.set_user_data(message.from_user.id,'gold',300)
			db.set_user_data(message.from_user.id,'can_shop',1)
			db.set_user_data(message.from_user.id,'can_job',1)
			db.set_user_data(message.from_user.id,'Level_task',1)
		await bot.send_message(message.from_user.id,text,reply_markup=kb_client_main_menu)
	else:
		await bot.send_message(message.from_user.id,"Это еще тебе не доступно")

class gardener_job_state(StatesGroup):
	point = State()

async def gardener_job(message:types.Message,state:FSMContext):
	if db.about_user(message.from_user.id)[0][9]>=2:
		point = random.randint(1,9)

		await gardener_job_state.point.set()
		async with state.proxy() as data:
			data['point'] = point
		kb = ReplyKeyboardMarkup(resize_keyboard = True)\
		.row(KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3"))\
		.row(KeyboardButton("4"),KeyboardButton("5"),KeyboardButton("6"))\
		.row(KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9"))\
		.add(KeyboardButton("Главное меню ⬅️"))
		with open(f'skin/mole_game/mole{point}.png','rb') as ph:
			await bot.send_photo(message.from_user.id,ph)

		await bot.send_message(message.from_user.id,"Где крот?",reply_markup = kb)
	else:
		await bot.send_message(message.from_user.id,"Вам это пока недоступно")

#db.set_user_data(message.from_user.id,"gold",user_data[12]+b_account_data["on_account"])
async def gardener_job_pick(message:types.Message,state:FSMContext):
	if message.text not in '123456789' and message.text!='Главное меню ⬅️' :
		await bot.send_message(message.from_user.id,"Используй кнопки!")
	elif message.text != 'Главное меню ⬅️':
		async with state.proxy() as data:
			point = data['point']
			if int(message.text) == point:
				user_data = db.about_user(message.from_user.id)[0]
				salary = random.randint(50,100)
				db.set_user_data(message.from_user.id,"gold",user_data[12]+salary)
				await bot.send_message(message.from_user.id,f'Ее ты попал, и заработал {salary} тугрик')
				if user_data[9] == 2 and True:
					db.set_user_data(message.from_user.id,'Level_task',3)
					db.set_user_data(message.from_user.id,'can_map','Москва')
					db.set_user_data(message.from_user.id,'can_shop',2)										
					db.set_user_data(message.from_user.id,'gold',user_data[12]+500)
					await state.finish()
					return await bot.send_message(message.from_user.id,'Задание выполнено!\n\nНаграда:\n1.500 золота🥇\n2.Разблокирована карта!',reply_markup = ReplyKeyboardMarkup(resize_keyboard = True).row(KeyboardButton('Главное меню ⬅️'),KeyboardButton('Садовник 🌳')))
					
			else:
				await bot.send_message(message.from_user.id,'Ну и мазила...')
			await state.finish()
			await gardener_job(message,state)
	else:
		await state.finish()
		await commands_start(message)

class set_my_map(StatesGroup):
	new_map = State()

async def show_map(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[6]==0:
		await bot.send_message(message.from_user.id,"Это тебе еще не доступно")
	else:
		await set_my_map.new_map.set()
		await bot.send_photo(message.from_user.id,"AgACAgIAAxkBAAIs42MBYsX89uO6p3WxWZHV9ik8BRKpAAKSwjEbcu0JSLqpnJ86xRGaAQADAgADcwADKQQ",f'{user_data[1]},сейчас ты в городе "{user_data[6]}"\nВыбери куда ты хочешь поехать',reply_markup = pick_map_menu(user_data[6]))

async def pick_new_map (message:types.Message,state:FSMContext):
	user_data = db.about_user(message.from_user.id)[0]
	user_map = user_data[6]
	new_map = message.text
	if user_data[23] < 4 and new_map == 'Сочи':
		await bot.send_message(message.from_user.id,'Это тебе еще не доступно')
		return await state.finish()
	if new_map == "Назад":
		await state.finish()
		await commands_start(message)
	if new_map != user_map:
		if new_map in ("Москва","Питер","Сочи"):
			await state.finish()
			db.set_user_data(message.from_user.id,'can_map',f'{new_map}')
			await bot.send_message(message.from_user.id,f"Ты отправился в город {new_map}!")
			await commands_start(message)
	elif new_map == user_map:
		await bot.send_message(message.from_user.id,"Вы и так в этом городе, выберите другой или выйдитие в главное меню")
	else:
		await bot.send_message(message.from_user.id,"Пользуйся клавиатурой!")

class get_gold(StatesGroup):
	need_get_gold = State()

class balance(StatesGroup):
	need_balance = State()

class balance_gold(StatesGroup):
	need_balance = State()



#@dp.message_handler(commands=['Пополнить баланс 💳']) 
async def up_balance(message : types.Message):
	await bot.send_message(message.from_user.id,'💳 Введите сумму в рублях\n1💎= 1 рубль ',reply_markup=kb_client_main_menu)
	await balance.need_balance.set()


async def balance_uper_pick (message:types.Message, state: FSMContext):
	if message.text!="Главное меню ⬅️":
		if message.chat.type == 'private':
			if is_number(message.text) and int(message.text)>=10:
				await state.finish()
				kb = InlineKeyboardMarkup()\
				.add(InlineKeyboardButton(text = "Пополнить через QIWI",callback_data = f"balance_uper_ {(message.text)}"))\
				#.add(InlineKeyboardButton(text = "Пополнить другим способом",callback_data = "another_way_pay_"))

				await bot.send_message(message.from_user.id,f'Вы хотитите пополнить баланс на {message.text} руб.\nВыберите способ оплаты:',reply_markup = kb)
			
			elif int(message.text)<10:
				await bot.send_message(message.from_user.id,"Минимальная сумма 10 руб.")
			else:
				await bot.send_message(message.from_user.id,"Введите целое число")			
			
	else:
		await state.finish()
		await main_menu()
		await bot.send_message(message.from_user.id,'Главное меню ⬅️')	

async def another_way_pay (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Украина:\nMonoBank: 4035200042169406\n\nРоссия:\nПополнение через терминал киви: +7 999 901-02-12\nQIWI: +7 999 901-02-12\nТинькофф - 5536914160597518")
	await bot.send_message(callback.from_user.id,"ГЛАВНОЕ ИМЕТЬ ЧЕК, ЧТОБЫ МЫ МОГЛИ УБЕДИТЬСЯ ЧТО ЭТО ВЫ ОТПРАВИЛИ НАМ ДЕНЬГИ.",reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "Отправить чек", callback_data = "send_chek_another_way_")))

class another_way(StatesGroup):
	chek_way = State() 

async def send_chek_another_way (callback:types.CallbackQuery):
	await callback.message.delete()
	await another_way.chek_way.set()
	await bot.send_message(callback.from_user.id,"Отправьте скриншот или фотографию чека после этого сообщения")

async def take_chek_another_way (message:types.Message, state = FSMContext):
	if message.content_type =='photo':
		await state.finish()
		kb = InlineKeyboardMarkup().add(\
			InlineKeyboardButton(text = "Пополнить баланс пользователя",callback_data = f'give_chek_gold_ {message.from_user.id}'),InlineKeyboardButton("Закрыть эту заявку",callback_data = f"otklon_chek_gold_ {message.from_user.id}"))
		
		await bot.send_photo(admin_chat_id,message.photo[0].file_id,f'Пользователь с id:{message.from_user.id} отправил чек',reply_markup = kb)
		await bot.send_message(message.from_user.id,'Спасибо, ожидайте! Выполняется проверка отправленного чека. Проверка занимает до 24 часов.')
	else:
		if message.text != "Главное меню ⬅️":
			await bot.send_message(message.from_user.id,'Пожалуйста отправьте чек или выйдите в главное меню')
		else:
			await state.finish()
			await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)
class give_gold_check(StatesGroup):
	cnt_gold = State() 
async def give_chek_gold (callback:types.CallbackQuery):
	global id_gold_give_chek
	id_gold_give_chek = callback['data'].replace('give_chek_gold_ ','')
	await bot.send_message(admin_chat_id,f"Сколько р. начислить id:{id_gold_give_chek}?")
	await give_gold_check.cnt_gold.set()

async def cnt_give_chek_gold (message:types.Message, state=FSMContext):
	global id_gold_give_chek
	if (str(message.text)).lower() != ("отмена"): 
		if is_number(message.text):
			await state.finish()
			user_money = db.user_money(id_gold_give_chek)
			db.set_money(id_gold_give_chek,user_money+int(message.text))
			await bot.send_message(admin_chat_id,f"Пользователю с id:{id_gold_give_chek} было зачислено {message.text} р.")
			await bot.send_message(id_gold_give_chek,f'Ваш чек проверели и зачислили на ваш счет {message.text} р.')
		else:
			await bot.send_message(admin_chat_id,'Введите целое число')
	else:
		await state.finish()
		await bot.send_message(admin_chat_id,"Пополнение отменено")

async def otklon_chek_gold (callback:types.CallbackQuery):
	await callback.message.delete()
	id_gold_del_chek = callback['data'].replace('otklon_chek_gold_ ','')
	await bot.send_message(admin_chat_id,f"Заявка от id:{id_gold_del_chek} на пополнение закыта")

	await bot.send_message(id_gold_del_chek,"Ваша заявка на пополнение баланса по чеку закрыта\nЕсли произошла ошибка, обратитесь в тех.поддержку")








async def balance_uper(message: types.CallbackQuery,):
	callback = message
	messagetext = callback['data'].replace('balance_uper_ ','')
	await callback.message.delete()

	global message_money
	message_money = int(messagetext)
	comment = str(message.from_user.id)+"_"+str(random.randint(1000,9999))
	bill = p2p.bill(amount = message_money,lifetime=15,comment=comment)


	db.add_check(message.from_user.id,message_money,bill.bill_id)

	await bot.send_message(message.from_user.id,f"Вам нужно отправить {message_money} руб. на наш счет киви\nСсылку: {bill.pay_url}\nУказав комментарий к оплате: {comment}",reply_markup=buy_menu(url=bill.pay_url,bill=bill.bill_id))




#@dp.message_handler(commands=['Пополнить 🥇])пополнение голды
async def up_my_gold(message : types.Message):
	await bot.send_message(message.from_user.id,'🥇 Введите количество золота для пополнения',reply_markup=kb_client_main_menu)
	await balance_gold.need_balance.set()


async def gold_uper(message: types.Message, state: FSMContext):
	if message.text!="Главное меню ⬅️":
		if message.chat.type == 'private':
			if is_number(message.text):
				if int(message.text)>=10:
					cur_money = db.user_money(message.from_user.id)
					need_gold = round(int(message.text)/100*70)
					global total_gold
					total_gold=message.text

					if cur_money < need_gold:
						
						await bot.send_message(message.from_user.id,f"Стоимость покупки {message.text} золота составляет {need_gold} руб.\nНа вашем счете недостаточно средств. Пополните баланс.")
					else:
						await bot.send_message(message.from_user.id,f'С вашего счета будет списано{need_gold} руб. за {message.text} золота.',reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Подтвердить',callback_data = "buy_need_gold_")))
						await state.finish()

				else:

					await bot.send_message(message.from_user.id,"Можно купить минимум 10 золота")
			else:
				await bot.send_message(message.from_user.id,"Введите целое число")
			
	else:
		await state.finish()
		await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)

async def buy_need_gold(message:types.CallbackQuery):
	global total_gold
	callback = message
	cur_money = db.user_money(message.from_user.id)
	need_gold = round(int(total_gold)/100*70)
	user_gold = db.user_gold(message.from_user.id)
	all_time_gold = db.user_gold_all_time(message.from_user.id)
	db.set_money(message.from_user.id, cur_money-need_gold)
	db.set_gold(message.from_user.id, user_gold+int(total_gold))
	db.set_gold_all_time(message.from_user.id,all_time_gold +int(total_gold))
	await callback.message.delete()
	await bot.send_message(message.from_user.id,f"Вы купили {total_gold} золота за {need_gold} руб.")
	if db.user_top_week_exists(message.from_user.id)==False:
		db.add_top_week(message.from_user.id)
		db.set_gold_top_week(message.from_user.id,int(total_gold))

	elif db.user_top_week_exists(message.from_user.id):
		top_week_gold = db.user_gold_top_week(message.from_user.id)
		db.set_gold_top_week(message.from_user.id,top_week_gold+int(total_gold))

	if db.user_top_month_exists(message.from_user.id)==False:
		db.add_top_month(message.from_user.id)
		db.set_gold_top_month(message.from_user.id,int(total_gold))

	elif db.user_top_month_exists(message.from_user.id):
		top_month_gold = db.user_gold_top_week(message.from_user.id)
		db.set_gold_top_month(message.from_user.id,top_month_gold+int(total_gold))




#@dp.message_handler(commands=['Вывод 🥇])вывод голды
async def get_my_gold(message : types.Message):
	await bot.send_message(message.from_user.id,'🥇 Введите количество золота для вывода',reply_markup=kb_client_main_menu)
	await get_gold.need_get_gold.set()

async def gold_geter(message: types.Message, state: FSMContext):
	if message.text!="Главное меню ⬅️":
		if message.chat.type == 'private':
			if is_number(message.text):
				if int(message.text)>=50:
					cur_gold = db.user_gold(message.from_user.id)
					#need_gold = round(int(message.text)/100*70)
					if cur_gold < int(message.text):
						await bot.send_message(message.from_user.id,"У вас недостаточно золота")
					else:
						async with state.proxy() as data:
							data['need_get_gold'] = message.text
						global gold_need_to_get
						gold_need_to_get = int(message.text)

						#user_gold = db.user_gold(message.from_user.id)
						#db.set_gold(message.from_user.id, user_gold-int(message.text))
						#await bot.send_message(message.from_user.id,f"Вы вывели {message.text} золота")
						await state.finish()
						await ways_gold_get_start(message)
				else:

					await bot.send_message(message.from_user.id,"Минимальная сумма 50 золота")
			else:
				await bot.send_message(message.from_user.id,"Введите целое число")			
	else:
		await state.finish()
		await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)
########очередь
async def show_my_turn(message:types.Message):
	if db.user_turn_exists(message.from_user.id):
		data = db.user_turn_data(message.from_user.id)
		await bot.send_message(message.from_user.id,f'Ваша очередь:\n{data[2]}G - №{data[0]}')
	else:
		await bot.send_message(message.from_user.id,'У вас нет предметов на вывод!')
######################################МЕНЮ ВЫВОД ГОЛДЫ#####################################################
async def ways_gold_get_start (message:types.Message):
	await bot.send_message(message.from_user.id,"Выберите предмет для вывода:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Оружие",callback_data = "guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Наклейки",callback_data = "stikers_gold_geter_"))\
		.add(InlineKeyboardButton(text = 'Брелки',callback_data = 'trinket_gold_geter_')))	


async def guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите категорию оружия:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Regular",callback_data = "regular_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "StatTrack",callback_data = "stattrack_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = 'Назад',callback_data = 'back_ways_gold_get_start_')))	


async def stikers_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()	
	await bot.send_message(callback.from_user.id,"Выберите качество наклеек:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Arcane",callback_data = "arcane_stikers_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Legendary",callback_data = "legendary_stikers_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Epic",callback_data = 'epic_stikers_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Rare", callback_data = 'rare_stikers_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_ways_gold_get_start_')))

async def trinket_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите качество наклеек:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Arcane",callback_data = "arcane_trinket_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Legendary",callback_data = "legendary_trinket_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Epic",callback_data = 'epic_trinket_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Rare", callback_data = 'rare_trinket_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_ways_gold_get_start_')))

async def back_ways_gold_get_start (callback:types.CallbackQuery):
	await callback.message.delete()
	await ways_gold_get_start(callback) 	
#########################################ВИДЫ ОРУЖИЙ########################################################################
async def regular_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите качество оружия:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Arcane",callback_data = "arcane_regular_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Legendary",callback_data = "legendary_regular_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Epic",callback_data = 'epic_regular_guns_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Rare", callback_data = 'rare_regular_guns_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_guns_gold_geter_')))

async def stattrack_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите качество оружия:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Arcane",callback_data = "arcane_stattrack_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Legendary",callback_data = "legendary_stattrack_guns_gold_geter_"))\
		.add(InlineKeyboardButton(text = "Epic",callback_data = 'epic_stattrack_guns_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Rare", callback_data = 'rare_stattrack_guns_gold_geter_'))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_guns_gold_geter_')))

async def back_guns_gold_geter (callback:types.CallbackQuery):
	#await callback.message.delete()
	await guns_gold_geter(callback) 	
##############################################ALL GUNS#########################################################################
async def arcane_regular_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "F/S 'Venom'",callback_data = "Gold_geter_pick F/S 'Venom'"),InlineKeyboardButton(text = "UMP45 'Beast'",callback_data ="Gold_geter_pick UMP45 'Beast'" ))\
		.add(InlineKeyboardButton(text = "P350 'Forest Spirit'",callback_data = "Gold_geter_pick P350 'Forest Spirit'"),InlineKeyboardButton(text = "P90 'Samurai'",callback_data = "Gold_geter_pick P90 'Samurai'"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_to_regular_guns_gold_geter_')))

async def legendary_regular_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()	
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "UMP45 'Winged'",callback_data = "Gold_geter_pick UMP45 'Winged'"),InlineKeyboardButton(text = "MP7 'Arcade'",callback_data ="Gold_geter_pick MP7 'Arcade'" ))\
		.add(InlineKeyboardButton(text = "MP7 'Lich'",callback_data = "Gold_geter_pick MP7 'Lich'"),InlineKeyboardButton(text = "TEC-9 'Fable'",callback_data = "Gold_geter_pick TEC-9 'Fable'"))\
		.add(InlineKeyboardButton(text = "M4 'Lizard'",callback_data = "Gold_geter_pick M4'Lizard'"),InlineKeyboardButton(text = "SM1014 'Necromancer'",callback_data = "Gold_geter_pick SM1014 'Necromancer'"))\
		.add(InlineKeyboardButton(text = "G22 'Frost Wyrm'",callback_data = "Gold_geter_pick G22 'Frost Wyrm'"),InlineKeyboardButton(text = "TEC-9 'Fable'",callback_data = "Gold_geter_pick TEC-9'Fable'"))\
		.add(InlineKeyboardButton(text = "M4 'Night Wolf'",callback_data = "Gold_geter_pick M4 'Night Wolf'"),InlineKeyboardButton(text = "AWM 'Dragon'",callback_data = "Gold_geter_pick AWM 'Dragon'"))\
		.add(InlineKeyboardButton(text = "USP 'Chameleon'",callback_data = "Gold_geter_pick USP 'Chameleon'"),InlineKeyboardButton(text = "M60 'Crunge'",callback_data = "Gold_geter_pick M60 'Crunge'"))\
		.add(InlineKeyboardButton(text = "Desers Eagle 'Orochi'",callback_data = "Gold_geter_pick Desers Eagle 'Orochi'"),InlineKeyboardButton(text = "M4 'Revival'",callback_data = "Gold_geter_pick M4 'Revival'"))\
		.add(InlineKeyboardButton(text = "AKR12 '4 Years'",callback_data = "Gold_geter_pick AKR12 '4 Years'"),InlineKeyboardButton(text = "F/S 'Rush'",callback_data = "Gold_geter_pick F/S 'Rush'"))
		.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_to_regular_guns_gold_geter_')))

async def epic_regular_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "P350 '4 Years'",callback_data = "Gold_geter_pick P350 '4 Years'"),InlineKeyboardButton(text = "UMP45 'White Carbone'",callback_data ="Gold_geter_pick UMP45 'White Carbone'" ))\
		.add(InlineKeyboardButton(text = "UMP45 'Gas'",callback_data = "Gold_geter_pick UMP45 'Gas'"),InlineKeyboardButton(text = "P90 'Iron Will'",callback_data = "Gold_geter_pick P90 'Iron Will'"))\
		.add(InlineKeyboardButton(text = "P350 'Neon'",callback_data = "Gold_geter_pick P350 'Neon'"),InlineKeyboardButton(text = "UMP45 'Cyberpunk'",callback_data = "Gold_geter_pick UMP45 'Cyberpunk'"))\
		.add(InlineKeyboardButton(text = "P90 'Ghoul'",callback_data = "Gold_geter_pick P90 'Ghoul'"),InlineKeyboardButton(text = "MP5 'Reactor'",callback_data = "Gold_geter_pick MP5 'Reactor'"))\
		.add(InlineKeyboardButton(text = "MP7 '2 Years'",callback_data = "Gold_geter_pick MP7 '2 Years'"),InlineKeyboardButton(text = "M4 'Predator'",callback_data = "Gold_geter_pick M4 'Predator'"))\
		.add(InlineKeyboardButton(text = "G22 'Monster'",callback_data = "Gold_geter_pick G22 'Monster'"),InlineKeyboardButton(text = "M40 'Winter Track'",callback_data = "Gold_geter_pick M40 'Winter Track'"))\
		.add(InlineKeyboardButton(text = "USP 'Stone Cold'",callback_data = "Gold_geter_pick USP 'Stone Cold'"),InlineKeyboardButton(text = "Назад",callback_data = "back_to_regular_guns_gold_geter_")))

async def rare_regular_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "F/S 'Zone'",callback_data = "Gold_geter_pick F/S 'Zone'"),InlineKeyboardButton(text = "MP5 'Northern Fury'",callback_data ="Gold_geter_pick MP5 'Northern Fury'" ))\
		.add(InlineKeyboardButton(text = "SM1014 'Arctic'",callback_data = "Gold_geter_pick SM1014 'Arctic'"),InlineKeyboardButton(text = "TEC-9 'Reactor'",callback_data = "Gold_geter_pick TEC-9 'Reactor'"))\
		.add(InlineKeyboardButton(text = "MP5 '4 Years'",callback_data = "Gold_geter_pick MP5 '4 Years'"),InlineKeyboardButton(text = "AWM 'Polar Night'",callback_data = "Gold_geter_pick AWM 'Polar Night'"))\
		.add(InlineKeyboardButton(text = "G22 'White Carbone'",callback_data = "Gold_geter_pick G22 'White Carbone'"),InlineKeyboardButton(text = "MP5 'Project Z9'",callback_data = "Gold_geter_pick MP5 'Project Z9'"))\
		.add(InlineKeyboardButton(text = "M40 'Acrtic'",callback_data = "Gold_geter_pick M40 'Acrtic'"),InlineKeyboardButton(text = "MP7 'Winter Sport'",callback_data = "Gold_geter_pick MP7 'Winter Sport'"))\
		.add(InlineKeyboardButton(text = "Desert Eagle 'Morgan'",callback_data = "Gold_geter_pick Desert Eagle 'Morgan'"),InlineKeyboardButton(text = "USP '2 Years'",callback_data = "Gold_geter_pick USP '2 Years'"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_regular_guns_gold_geter_")))

async def back_to_regular_guns_gold_geter (callback = types.CallbackQuery):
	await regular_guns_gold_geter(callback)
########stattrack guns###
async def cant_found_items (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Не найдены предметы в этой категории")


async def arcane_stattrack_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Не найдены предметы в этой категории")#reply_markup = InlineKeyboardMarkup()\
		#.add(InlineKeyboardButton(text = "F/S 'Venom'",callback_data = "Gold_geter_pick F/S 'Venom'"),InlineKeyboardButton(text = "UMP45 'Beast'",callback_data ="Gold_geter_pick UMP45 'Beast'" ))\
		#.add(InlineKeyboardButton(text = "P350 'Forest Spirit'",callback_data = "Gold_geter_pick P350 'Forest Spirit'"),InlineKeyboardButton(text = "P90 'Samurai'",callback_data = "Gold_geter_pick P90 'Samurai'"))\
		#.add(InlineKeyboardButton(text = "Назад",callback_data = 'back_to_regular_guns_gold_geter_')))

async def epic_stattrack_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "FAMAS 'Beagle'",callback_data = "Gold_geter_pick FAMAS 'Beagle'"),InlineKeyboardButton(text = "M40 'Stream Beast'",callback_data ="Gold_geter_pick M40 'Stream Beast'" ))\
		.add(InlineKeyboardButton(text = "UMP45 'Cerberus'",callback_data = "Gold_geter_pick UMP45 'Cerberus'"),InlineKeyboardButton(text = "UMP45 'Spirit'",callback_data = "Gold_geter_pick UMP45 'Spirit'"))\
		.add(InlineKeyboardButton(text = "MP7 'Place'",callback_data = "Gold_geter_pick MP7 'Place'"),InlineKeyboardButton(text = "FAMAS 'Anger'",callback_data = "Gold_geter_pick FAMAS 'Anger'"))\
		.add(InlineKeyboardButton(text = "USP 'Pisces'",callback_data = "Gold_geter_pick USP 'Pisces'"),InlineKeyboardButton(text = "FN FAL 'Tactical'",callback_data = "Gold_geter_pick FN FAL 'Tactical'"))\
		.add(InlineKeyboardButton(text = "F/S 'Wraith'",callback_data = "Gold_geter_pick F/S 'Wraith'"),InlineKeyboardButton(text = "ARK12 'Carbone'",callback_data = "Gold_geter_pick ARK12 'Carbone'"))\
		.add(InlineKeyboardButton(text = "FabM 'Parrot'",callback_data = "Gold_geter_pick Desert FabM 'Parrot'"),InlineKeyboardButton(text = "M4 'Grand Prix'",callback_data = "Gold_geter_pick M4 'Grand Prix'"))\
		.add(InlineKeyboardButton(text = "M40 'Quake'",callback_data = "Gold_geter_pick M40 'Quake'"),InlineKeyboardButton(text = "MP7 'Offroad'",callback_data = "Gold_geter_pick MP7 'Offroad'"))\
		.add(InlineKeyboardButton(text = "Desert Eagle 'Dragon\nGlass'",callback_data = "Gold_geter_pick Desert Eagle 'Dragon Glass'"),InlineKeyboardButton(text = "M60'Y-20 R.A.I.J.I.N'",callback_data = "Gold_geter_pick M60'Y-20 R.A.I.J.I.N'"))\
		.add(InlineKeyboardButton(text = "P90 'Z-50 F.U.J.I.N'",callback_data = "Gold_geter_pick P90 'Z-50 F.U.J.I.N'"),InlineKeyboardButton(text = "M4 'R.O.N.I.N. mk56'",callback_data = "Gold_geter_pick M4 'R.O.N.I.N. mk56'"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_regular_guns_gold_geter_")))

async def rare_stattrack_guns_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "FabM 'Reactor'",callback_data = "Gold_geter_pick FabM 'Reactor'"),InlineKeyboardButton(text = "AKR12 'Flow'",callback_data ="Gold_geter_pick AKR12 'Flow'" ))\
		.add(InlineKeyboardButton(text = "F/S 'Zone'",callback_data = "Gold_geter_pick F/S 'Zone'"),InlineKeyboardButton(text = "MP5 'Northern Fury'",callback_data = "Gold_geter_pick MP5 'Northern Fury'"))\
		.add(InlineKeyboardButton(text = "SM1014 'Acrtic'",callback_data = "Gold_geter_pick SM1014 'Acrtic'"),InlineKeyboardButton(text = "TEC-9 'Reactor'",callback_data = "Gold_geter_pick TEC-9 'Reactor'"))\
		.add(InlineKeyboardButton(text = "MP5 'Project Z9'",callback_data = "Gold_geter_pick MP5 'Project Z9'"),InlineKeyboardButton(text = "M40 'Arctic'",callback_data = "Gold_geter_pick M40 'Arctic'"))\
		.add(InlineKeyboardButton(text = "MP7 'Winter Sport'",callback_data = "Gold_geter_pick MP7 'Winter Sport'"),InlineKeyboardButton(text = "P350 'Rally'",callback_data = "Gold_geter_pick P350 'Rally'"))\
		.add(InlineKeyboardButton(text = "FAMAS 'Hull'",callback_data = "Gold_geter_pick FAMAS 'Hull'"),InlineKeyboardButton(text = "M110 'Transition'",callback_data = "Gold_geter_pick M110 'Transition'"))\
		.add(InlineKeyboardButton(text = "UMP45 'Shark'",callback_data = "Gold_geter_pick UMP45 'Shark'"),InlineKeyboardButton(text = "MP7 'Banana'",callback_data = "Gold_geter_pick MP7 'Banana'"))\
		.add(InlineKeyboardButton(text = "Desert Eagle 'Ace'",callback_data = "Gold_geter_pick Desert Eagle 'Ace'"),InlineKeyboardButton(text = "P350 'Oni'",callback_data = "Gold_geter_pick P350 'Oni'"))\
		.add(InlineKeyboardButton(text = "SM1014 'Wave'",callback_data = "Gold_geter_pick SM1014 'Wave'"),InlineKeyboardButton(text = "M40 'Beagle'",callback_data = "Gold_geter_pick M40 'Beagle'"))\
		.add(InlineKeyboardButton(text = "M4 'PRO'",callback_data = "Gold_geter_pick M4 'PRO'"),InlineKeyboardButton(text = "G22 'Carbone'",callback_data = "Gold_geter_pick G22 'Carbone'"))\
		.add(InlineKeyboardButton(text = "TEC-9 'Tropic'",callback_data = "Gold_geter_pick TEC-9 'Tropic'"),InlineKeyboardButton(text = "M4 'Demon'",callback_data = "Gold_geter_pick M4 'Demon'"))\
		.add(InlineKeyboardButton(text = "UMP45 'Geometric'",callback_data = "Gold_geter_pick UMP45 'Geometric'"),InlineKeyboardButton(text = "FabM 'Flight'",callback_data = "Gold_geter_pick FabM 'Flight'"))\
		.add(InlineKeyboardButton(text = "Desert Eagle 'Red\nDragon'",callback_data = "Gold_geter_pick Desert Eagle 'Red Dragon'"),InlineKeyboardButton(text = "P350 'Autumn'",callback_data = "Gold_geter_pick P350 'Autumn'"))\
		.add(InlineKeyboardButton(text = "AWM 'Scratch'",callback_data = "Gold_geter_pick AWM 'Scratch'"),InlineKeyboardButton(text = "AKR12 'Pixel\nCamouflage'",callback_data = "Gold_geter_pick AKR12 'Pixel Camouflage'"))\
		.add(InlineKeyboardButton(text = "SM1014 'Pathfinder'",callback_data = "Gold_geter_pick SM1014 'Pathfinder'"),InlineKeyboardButton(text = "M4A1 'Kitsune'",callback_data = "Gold_geter_pick M4A1 'Kitsune'"))\
		.add(InlineKeyboardButton(text = "Desert Eagle 'Predator'",callback_data = "Gold_geter_pick Desert Eagle 'Predator'"),InlineKeyboardButton(text = "AWM 'Phoenix'",callback_data = "Gold_geter_pick AWM 'Phoenix'"))\
		.add(InlineKeyboardButton(text = "ARK 'Nano'",callback_data = "Gold_geter_pick ARK 'Nano'"),InlineKeyboardButton(text = "AKR 'Carbon'",callback_data = "Gold_geter_pick AKR 'Carbon'"))\
		.add(InlineKeyboardButton(text = "M110 'Z-07 M.A.R.K.S.M.A.N'",callback_data = "Gold_geter_pick M110 'Z-07 M.A.R.K.S.M.A.N'"),InlineKeyboardButton(text = "AKR12 'Armored'",callback_data = "Gold_geter_pick AKR12 'Armored'"))\
		.add(InlineKeyboardButton(text = "F/S 'Enforcer'",callback_data = "Gold_geter_pick F/S 'Enforcer'"),InlineKeyboardButton(text = "AKR12 'Transistor'",callback_data = "Gold_geter_pick AKR12 'Transistor'"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_regular_guns_gold_geter_")))

async def back_to_stattrack_guns_gold_geter (callback = types.CallbackQuery):
	await stattrack_guns_gold_geter(callback)
##########STIKERS PICK#####################################################

async def epic_stikers_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Sector B",callback_data = "Gold_geter_pick Sector B"),InlineKeyboardButton(text = "Brick",callback_data ="Gold_geter_pick Brick" ))\
		.add(InlineKeyboardButton(text = "Carpet",callback_data = "Gold_geter_pick Carpet"),InlineKeyboardButton(text = "4 Years Metallic",callback_data = "Gold_geter_pick 4 Years Metallic"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_stikers_gold_geter_")))

async def rare_stikers_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "DEagle Master",callback_data = "Gold_geter_pick DEagle Master"),InlineKeyboardButton(text = "Not Today",callback_data ="Gold_geter_pick Not Today" ))\
		.add(InlineKeyboardButton(text = "Lucky Start",callback_data = "Gold_geter_pick Lucky Start"),InlineKeyboardButton(text = "Pewnguin",callback_data = "Gold_geter_pick Pewnguin"))\
		.add(InlineKeyboardButton(text = "AWM Master",callback_data = "Gold_geter_pick AWM Master"),InlineKeyboardButton(text = "Spare Gold",callback_data = "Gold_geter_pick Spare Gold"))\
		.add(InlineKeyboardButton(text = "Headshot Zone",callback_data = "Gold_geter_pick Headshot Zone"),InlineKeyboardButton(text = "Назад",callback_data = "back_to_stikers_gold_geter_")))


async def back_to_stikers_gold_geter (callback:types.CallbackQuery):
	await stikers_gold_geter(callback)

###############
async def epic_trinket_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Santa Helper",callback_data = "Gold_geter_pick Santa Helper"),InlineKeyboardButton(text = "4 Years Silver",callback_data ="Gold_geter_pick 4 Years Silver" ))\
		.add(InlineKeyboardButton(text = "Phoenix",callback_data = "Gold_geter_pick Phoenix"),InlineKeyboardButton(text = "Gift Thief",callback_data = "Gold_geter_pick Gift Thief"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_trinket_gold_geter_")))

async def rare_trinket_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,"Выберите предмет из списка:",reply_markup = InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = "Dummy",callback_data = "Gold_geter_pick Dummy"),InlineKeyboardButton(text = "Mr Bowler",callback_data ="Gold_geter_pick Mr Bowler" ))\
		.add(InlineKeyboardButton(text = "Baby Penguin",callback_data = "Gold_geter_pick Baby Penguin"),InlineKeyboardButton(text = "Gingerbread",callback_data = "Gold_geter_pick Gingerbread"))\
		.add(InlineKeyboardButton(text = "Gift Catcher",callback_data = "Gold_geter_pick Gift Catcher"),InlineKeyboardButton(text = "Daruma",callback_data = "Gold_geter_pick Daruma"))\
		.add(InlineKeyboardButton(text = "Imperial Coin",callback_data = "Gold_geter_pick Imperial Coin"),InlineKeyboardButton(text = "Kitsune",callback_data = "Gold_geter_pick Kitsune"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_trinket_gold_geter_")))


async def back_to_trinket_gold_geter (callback:types.CallbackQuery):
	await trinket_gold_geter(callback)


class photo_gold_geter(StatesGroup):
	photo = State()
async def total_gold_geter(callback = types.CallbackQuery):
	if db.user_turn_exists(callback.from_user.id):
		await callback.message.delete()
		await bot.send_message(callback.from_user.id,'Вы уже стоите в очереди, дождитесь ответа на предыдущую заявку')
	else:
		await callback.message.delete()
		global price_gold_geter
		price_gold_geter = gold_need_to_get+(((gold_need_to_get)/100)*25) +(random.randint(5,15)/100)
		y = (callback['data']).replace('Gold_geter_pick','')
		text = f"🌟Отлично!\n\nТеперь вам необходимо зайти в Standoff 2 и сделать скриншот, где выставлен {y} на рынке за {price_gold_geter} G.\n\n❗Не забудьте поставить галочку на рынке:'Только мои запросы'!\n\nКогда все будет сделано, отправьте скриншот в этот диалог.\nПример сверху ⬆"
		#await bot.send_message(admin_chat_id,y)
		await bot.send_photo(callback.from_user.id,'AgACAgIAAxkBAAIdyGLMgvk4wIHscrx4yVvIBj8kVm4JAAKwwDEbzKtoSgPhqjm1LhE-AQADAgADcwADKQQ',text)
		await photo_gold_geter.photo.set()

async def send_order_gold (message: types.Message, state: FSMContext):
	if message.content_type == 'photo':
		await state.finish()
		global price_gold_geter
		db.add_user_turn(message.from_user.id)
		db.set_user_turn(message.from_user.id,gold_need_to_get)
		cur_gold = db.user_gold(message.from_user.id)
		db.set_gold(message.from_user.id,int(cur_gold)-int(gold_need_to_get))
		id_turn = db.user_turn_data(message.from_user.id)[0]
		await bot.send_message(message.from_user.id,f'💫 Ваш запрос на вывод добавлен, ожидайте.\n\n⏱ Вы {id_turn} в очереди')
		await bot.send_photo(admin_chat_id,message.photo[0].file_id,f'Пользователь с id:{message.from_user.id},заказал вывод {gold_need_to_get} G\nЕму необходимо было поставить цену в {price_gold_geter} G',reply_markup=\
			InlineKeyboardMarkup().add(InlineKeyboardButton(text = 'Золото передано',callback_data = f'finish_gold_geter {message.from_user.id,gold_need_to_get,id_turn}'),InlineKeyboardButton(text = 'Вернуть ему золото',callback_data = f'money_back_gold_geter {message.from_user.id,gold_need_to_get,id_turn}')))
		db.set_gold_calls(message.from_user.id,1)
	else:
		if message.text != "Главное меню ⬅️":
			await bot.send_message(message.from_user.id,'Пожалуйста отправьте скриншот или выйдите в главное меню')
		else:
			await state.finish()
			await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)

async def finish_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	x = callback['data']
	y = (callback['data'].replace('finish_gold_geter ','')).split(',')
	id_user = y[0]
	need_gold = y[1]
	id_turn = y [2]
	kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text = 'Да',callback_data=f'Total_gold {x}'),InlineKeyboardButton(text = 'Нет,вернуть ему золото',callback_data = f'money_back_gold_geter {id_user,need_gold,id_turn}'))
	await bot.send_message(admin_chat_id,f'Вы уверенны что передали золото, и хотете закрыть заявку?\nid:{id_user}\n{need_gold}G',reply_markup = kb )


async def total_finish_gold_geter(callback:types.CallbackQuery):
	await callback.message.delete()
	data = ((((callback['data'].replace('finish_gold_geter ','')).replace('Total_gold ','')).replace('(','')).replace(')','')).split(',')
	#await bot.send_message(admin_chat_id,data)

	id_user = data[0]
	need_gold = data[1]
	id_turn = data [2]
	db.delete_user_turn(id_turn)
	await bot.send_message(admin_chat_id,f'Заявка пользователя id:{id_user} на {need_gold}G была закрыта')
	await bot.send_message(id_user,'Вам передали золото и сняли с очереди')
	db.set_gold_calls(id_user,0)


async def money_back_gold_geter (callback:types.CallbackQuery):
	await callback.message.delete()
	data = (((callback['data'].replace('money_back_gold_geter ','')).replace('(','')).replace(')','')).split(',')
	id_user = data[0]
	#id_user = int(id_user)
	need_gold = data[1]
	id_turn = data [2]
	user_gold = db.user_gold(id_user)
	db.set_gold(id_user,user_gold+int(user_gold))
	db.delete_user_turn(id_turn)
	await bot.send_message(admin_chat_id,f'Вы вернули пользователю с id:{id_user}\n{need_gold} золота')
	await bot.send_message(id_user,'Средства вернулись обратно на ваш баланс')
	db.set_gold_calls(id_user,0)
































#Игры на золото
async def gold_games(message : types.Message):
	if db.about_user(message.from_user.id)[0][6] == "Сочи":
		await bot.send_message(message.from_user.id,'Добро пожаловать в наше казино, тут вы можете поднять целое состояние, ну или остататься без трусов)\nВыберете игру 🎲:',reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Башня',callback_data = "game_tawer_")).add(InlineKeyboardButton(text='JackPot',callback_data = "game_JackPot_text_")))
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")
async def game_tawer(callback : types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		await callback.message.delete()
		text = 'Башня - это игра, где вы делаете ставку в золоте и угадываете направление башни, поднимаясь все выше. Чем выше вы поднимитесь, тем больше награда. Если вы не угадали, игра заканчивается. Максимальной коэффициент выигрыша 3X.'
		await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Играть',callback_data = "start_game_tawer_")).add(InlineKeyboardButton(text = "Назад", callback_data = "back_to_gold_game_")))
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")

class gold_to_tawer(StatesGroup):
	gold = State()
async def start_game_tawer(callback: types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		await callback.message.delete()
		await gold_to_tawer.gold.set()
		await bot.send_message(callback.from_user.id,"Минимальная ставна 10G")
		await bot.send_message(callback.from_user.id,"Введите сумму ставки:",reply_markup = kb_client_main_menu)
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")

async def count_gold_to_tawer(message: types.Message, state: FSMContext):
	if db.about_user(message.from_user.id)[0][6] == "Сочи":
		user_gold = db.user_gold(message.from_user.id)
		if message.text == ('Главное меню ⬅️'):
			await state.finish()
			await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)
		elif message.text.isdigit()==False:
			await bot.send_message(message.from_user.id,"Введите целое число")
		elif int(int(message.text)**2)**0.5!=int(message.text):
			await bot.send_message(message.from_user.id,"Введите целое число")

		elif int(message.text)<10:
			await bot.send_message(message.from_user.id,"Минимальная сумма ставки 10G")
		elif user_gold >= int(message.text):
			db.set_gold(message.from_user.id, user_gold-int(message.text))
			#Сделали ставку
			db.set_user_data(message.from_user.id,'stavka',int(message.text))
			await state.finish()

			await show_me_game_tawer(message)
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")



async def show_me_game_tawer(message: types.Message):
	if db.about_user(message.from_user.id)[0][6] == "Сочи":
		cnt_tower_way = db.about_user(message.from_user.id)[0][18]
		if cnt_tower_way in (0,None):
			db.set_user_data(message.from_user.id,'tawer_way',1)
			cnt_tower_way = 1

		if cnt_tower_way > 1:
			await bot.send_message(message.from_user.id,"Чтобы продолжить играть, нажмите кнопку 'Лево' или 'Право'.\nА если хотите забрать средства, жмите кнопку 'забрать выигрыш'.",reply_markup = InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton(text='Лево',callback_data = "tawer_go_"),InlineKeyboardButton(text='Право',callback_data = "tawer_go_")).add(InlineKeyboardButton(text='Забрать выигрыш',callback_data = "tawer_take_my_money_")))
		else:
			db.set_user_data(message.from_user.id,'tawer_way',1)
			await bot.send_message(message.from_user.id,"Выберите направление башни",reply_markup = InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton(text='Лево',callback_data = "tawer_go_"),InlineKeyboardButton(text='Право',callback_data = "tawer_go_")))
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")

async def tawer_go(callback: types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		cnt_tower_way = db.about_user(callback.from_user.id)[0][18]
		gold_stavka = db.about_user(callback.from_user.id)[0][19]
		way = random.randint(0,1)
		if way == 0:
			await callback.message.delete()
			await bot.send_message(callback.from_user.id,"Упс, вам не повезло ☹️")
			db.set_user_data(callback.from_user.id,'tawer_way',0)
			db.set_user_data(callback.from_user.id,'stavka',0)
		elif way == 1 and cnt_tower_way == 1:
			await callback.message.delete()
			gold_stavka = int(gold_stavka*1.15)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")
			await show_me_game_tawer(callback)


		elif way == 1 and cnt_tower_way == 2:
			await callback.message.delete()
			gold_stavka = int(gold_stavka*1.5)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")
			await show_me_game_tawer(callback)	

		elif way == 1 and cnt_tower_way == 3:
			await callback.message.delete()
			gold_stavka = int(gold_stavka*1.75)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")
			await show_me_game_tawer(callback)	

		elif (way == 1) and (cnt_tower_way == 4):
			await callback.message.delete()

			gold_stavka = int(gold_stavka*2)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")	
			await show_me_game_tawer(callback)
		elif (way == 1) and (cnt_tower_way == 5):
			await callback.message.delete()
			gold_stavka = int(gold_stavka*2.5)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")	
			await show_me_game_tawer(callback)
		elif (way == 1) and (cnt_tower_way == 6):
			await callback.message.delete()
			gold_stavka = int(gold_stavka*3)
			db.set_user_data(callback.from_user.id,'stavka',gold_stavka)
			db.set_user_data(callback.from_user.id,'tawer_way',cnt_tower_way+1)
			await bot.send_message(callback.from_user.id,f"Поздравляем Вы выиграли {gold_stavka} золота")	
			await show_me_game_tawer(callback)
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")


 #Кнопка забрать выигрыш
async def tawer_take_my_money(callback: types.CallbackQuery):
	user_data = db.about_user(callback.from_user.id)[0]
	if user_data[6] == "Сочи":
		gold_stavka = db.about_user(callback.from_user.id)[0][19]
		await callback.message.delete()
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+gold_stavka)

		db.set_user_data(callback.from_user.id,'stavka',0)
		db.set_user_data(callback.from_user.id,'tawer_way',0)
		await bot.send_message(callback.from_user.id,f'Ты забрал с собой свой выигрыш ({user_data[19]} золота🥇)!Приходи еще!')
		if user_data[23] == 5:
			await bot.send_message(callback.from_user.id,"Молодец, ты выиграл и выполнил задание!\nТвоя награда\n1. 300 золота🥇\n2.Разблокирован бизнесс.Выйди в главное меню, чтобы узнать, что это")
			db.set_user_data(callback.from_user.id,'can_bussines',1)
			db.set_user_data(callback.from_user.id,'Level_task',6)
			
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")

class bet_gold(StatesGroup):
	my_bet = State()

def pick_winner(lst,win):
	lst = sorted(lst)
	winners = []
	if win in range(1,lst[0]):
		winners.append(lst[0])
	for i in range(1,len(lst)):
		if win in range(lst[i-1],lst[i]):
			winners.append(lst[i])
	return winners




async def game_JackPot_text(callback:types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		await callback.message.delete()
		kb = InlineKeyboardMarkup(row_width=2)\
		.add(InlineKeyboardButton(text = 'Играть',callback_data = "game_JackPot_"))\
		.add(InlineKeyboardButton(text = "Назад",callback_data = "back_to_gold_game_"))
		text = "Режим JackPot - Это предельно простой, но очень интересный режим. Все участники вносят любую ставку золотом и образуется общий банк. Каждый участник получает свой шанс на выигрыш, зависящий от его ставки. Чем больше ставка, тем больше шанс выиграть. Но и с маленьким шансом есть возможность выиграть весь банк! Мы берём 10% за выигрыш."
		await bot.send_message(callback.from_user.id,text,reply_markup = kb)
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")

async def game_JackPot(callback:types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		kb_bet = InlineKeyboardMarkup(row_width=2)\
		.add(InlineKeyboardButton(text='Обновить',callback_data = "game_JackPot_"))\
		.add(InlineKeyboardButton(text='Сделать ставку',callback_data = "do_gold_bet_"))
		if db.bet_exists()==False:
			bank = 0
			await callback.message.delete()
			await bot.send_message(callback.from_user.id,f'Банк: {bank}G\nВремя: Ожидаем ставки',reply_markup = kb_bet)
		else :
			stop_t = datetime.datetime.strptime(db.JackPot_time_stop(), '%Y-%m-%d %H:%M:%S.%f')
			data_time =datetime.datetime.now() 
			if stop_t < data_time:
				bets = db.all_bet()
				chanse_list = []
				bank = 0
				for bet in bets:
					bank += int(bet[2])
					chanse_list.append(bet[2])
				winner_random = random.randint(1,int(bank))
				real_winner = pick_winner(chanse_list,winner_random)
				real_winner = [x[1] for x in bets if x[2] in real_winner]
				total_winner = real_winner[random.randint(0,len(real_winner)-1)]
				db.JackPot_time_set()
				user_gold = db.user_gold(total_winner)
				db.set_gold(total_winner, user_gold+int(bank*0.9))
				await bot.send_message(total_winner,f"Поздравляю, ты выиграл {int(bank*0.9)}G")
				await bot.send_message(callback.from_user.id,f'Банк: 0G\nВремя: Ожидаем ставки',reply_markup = kb_bet)

			else:			
				bets = db.all_bet()
				bets_str = ''
				bank = 0
				for bet in bets:
					bank += int(bet[2])
					bets_str = bets_str + f'{bet[1]} - {bet[2]}G | {bet[3]}%\n'
				delta = str(stop_t - data_time).split('.')[0]
				await callback.message.delete()
				await bot.send_message(callback.from_user.id,f'Банк: {bank}G\nВремя: {delta}\nИгроки:\n{bets_str}',reply_markup = kb_bet)
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")








async def do_gold_bet(callback:types.CallbackQuery):
	if db.about_user(callback.from_user.id)[0][6] == "Сочи":
		await callback.message.delete()
		await bot.send_message(callback.from_user.id,'Введите сумму ставки')
		await bet_gold.my_bet.set()
	else:
		await bot.send_message(callback.from_user.id,"Этого нет в твоем городе, открой карту")

def set_all_bets():
	bets = db.all_bet()
	bank = 0
	for bet in bets:
			bank += int(bet[2])
	for bet in bets:
		cur_bet = bet[2]
		div_win = bank/100
		win_chanse = int(cur_bet/div_win)
		if cur_bet == bank:
			win_chanse == 100
		db.set_win_chanse(bet[1],win_chanse)

async def count_gold_bet(message: types.Message, state: FSMContext):
	if db.about_user(message.from_user.id)[0][6] == "Сочи":
		if is_number(message.text):
			user_gold = db.user_gold(message.from_user.id)
			if int(message.text)<=user_gold:
				if db.user_bet_exists(message.from_user.id):
					user_last_bet = db.user_gold_bet(message.from_user.id)
					db.set_gold(message.from_user.id, user_gold-(int(message.text)))
					db.set_gold_bet(message.from_user.id,user_last_bet+int(message.text))
					set_all_bets()
					await bot.send_message(message.from_user.id,f"Вы сделали ставку в еще {message.text}G")
					await state.finish()
				else:
					if db.bet_exists() == False:
						start_game = datetime.datetime.now()
						stop_game = start_game + datetime.timedelta(minutes = 10)
						db.JackPot_time_start_add(start_game)
						db.JackPot_time_stop_add(stop_game)
					db.set_gold(message.from_user.id, user_gold-(int(message.text)))
					db.add_user_bet(message.from_user.id)
					db.set_gold_bet(message.from_user.id,int(message.text))
					set_all_bets()
					await bot.send_message(message.from_user.id,f"Вы сделали ставку в {message.text}G")
					await state.finish()

			else:
				await bot.send_message(message.from_user.id,'На вашем счете недостаточно средств')

		else:
			await bot.send_message(message.from_user.id,"Введите целове число")
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")

async def back_to_gold_game (callback:types.CallbackQuery):
	await callback.message.delete()
	await gold_games(callback)


async def donat_menu(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[3] != None:
		kb = ReplyKeyboardMarkup(resize_keyboard=True)\
		.row(KeyboardButton("Пополнить баланс 💳"),KeyboardButton("Донат Магазин 💎"))\
		.add(KeyboardButton("Главное меню ⬅️"))
		string = f"Добро пожаловать в раздел донат,{user_data[1]}!Сейчас на твоем счету {user_data[11]} 💎!"
		await bot.send_message(message.from_user.id,string,reply_markup = kb)
	else:
		await bot.send_message(message.from_user.id,"Это еще тебе не доступно!")


#async def donat_menu(message:types.Message)





#@dp.message_handler(commands=['Золото 🥇'])
async def pizza_open_command(message : types.Message):
	await bot.send_message(message.from_user.id,'Выберите действие в меню',reply_markup=kb_client_gold)

#@dp.message_handler(commands=['GJREGFDNM'])тут покупка
#async def pokupka(message : types.Message):
#	await bot.send_message(-1001547431503,"@" + message.from_user.username + ": " + message.text[6:])


#@dp.message_handler(commands=[menu])тут главное меню
async def main_menu(message : types.Message):
	await commands_start(message)


async def reviews(message : types.Message):
	await bot.send_message(message.from_user.id,'Наши отзывы: (тут будет ссылка на канал с отзывами)')

class schet_gold(StatesGroup):
	my_gold = State()

#@dp.message_handler(commands=['Посчитать 🥇'])
async def pizza_place_command(message : types.Message):
	await bot.send_message(message.from_user.id,"🥇 Введите количество золота",reply_markup=kb_client_main_menu)#,reply_markup=ReplyKeyboardRemove())
	await schet_gold.my_gold.set()



#Считает голду
#@dp.message_handler(state=FSMAdmin.name)
async def count_gold(message: types.Message, state: FSMContext):
	await bot.send_message(message.from_user.id, message.photo[0].file_id)
	if message.text == ('Главное меню ⬅️'):
		await state.finish()
		await bot.send_message(message.from_user.id,'Главное меню ⬅️',reply_markup=kb_client)
	elif message.text.isdigit()==False:
		await bot.send_message(message.from_user.id,"Введите целое число")
	elif int(int(message.text)**2)**0.5!=int(message.text):
		await bot.send_message(message.from_user.id,"Введите целое число")

	elif int(message.text)<10:

		await bot.send_message(message.from_user.id,"Можно купить минимум 10 золота")
	else:
		async with state.proxy() as data:
			data['schet_gold'] = message.text
		price = int(int(message.text)/100*70)
		await bot.send_message(message.from_user.id,'Цена за '+(message.text)+' золота, '+str(price) +' руб.')
		#await bot.send_message(-1001547431503,"Клиент с номером " + str(message.text) +  " хочет купить:"+Name_bay)

#@dp.message_handler(commands=['другие товары'])
async def other_staf(callback : types.CallbackQuery):
	if True:
		await bot.send_message(callback.from_user.id,'Доступных товаров пока нет') 
	else:
		cnt = 1
		read = await db.staf_read()
		lists = ''
		if db.other_staf_exists():
			for i in range(len(read)):
				lists = f'{lists}\n'+str(cnt)+'. '+read[i][1]
				cnt+=1
			await bot.send_message(callback.from_user.id,f'Список доступных товаров:{lists}',reply_markup = kb_for_staf)
		else:
			await bot.send_message(callback.from_user.id,"Доступных товаров пока нет")




#инлайн кнопка для других товаров
async def first_staf(message : types.CallbackQuery):
	read = await db.staf_read()
	ret = read[0]
	global name_ret
	name_ret = ret[1]
	#for ret in read:
	await message.message.delete()
	await bot.send_photo(message.from_user.id,ret[0],f"Название:{ret[1]}\nОписание: {ret[2]}",reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Купить',callback_data = "buy_first_staf_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_staf_")))

async def buy_first_staf(callback : types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 3500:
		db.delete_staf(name_ret)
		db.set_money(callback.from_user.id, user_money-3500)
		await bot.send_message(callback.from_user.id,f'Поздравляю вы купили этот товар!')
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')

async def back_to_staf(callback : types.CallbackQuery):
	await callback.message.delete()
	await other_staf(callback)

#async def pizza_menu_command(message : types.Message):
#
#	#await sqlite_db.sql_read(message)
#	read = await sqlite_db.sql_read2()
#	for ret in read:
#		await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена {ret[-1]}',disable_notification=True)
#		await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
#			add(InlineKeyboardButton(f'Купить {ret[1]}', callback_data=f'Send_bay {ret[1]}')),disable_notification=True)
#	await bot.send_message(message.from_user.id,'Вот список наших таваров, что бы купить нажмите кнопку под нужным товаром')

#кейсы kb_chests
async def chests(message : types.Message):
	await bot.send_message(message.from_user.id,'Выберите кейс из списка:',reply_markup =kb_chests )




#text_for_help = "1. Почему я пополняю в гривнах, а мне пришло меньше рублей, чем пишет в интернете?\n2. Сколько по времени выводят золото?\n3. Почему так долго проверяют чек?\n4. Почему мне не пришли деньги?\n5. Безопасно ли у вас покупать?\n6. Можно ли вам продать золото/кланы/аккаунт/скины?\n7. Почему так долго выводят золото?\n\nЕсли вы не смогли найти ответ, нажмите кнопку связаться"
#@dp.message_handler(message: types.Message)тех помощ
async def tech_help (message: types.Message):

	help_button = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Связаться',callback_data = "help_8_"))
	await bot.send_message(message.from_user.id,f'Ваш id:{message.from_user.id}\nХотите связаться с тех.поддержкой?',reply_markup=help_button)

	#await bot.send_message(message.from_user.id,text_for_help,reply_markup=kb_for_help)


################ИНЛАЙН КНОПКИ ТЕХ ПОМОЩИ#############
async def help_for_1(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Мы не являемся биржей валют, вы у нас покупаете золото, а не рубли. То есть, мы переводим ваши гривны в золото. После, золото в рубли.',reply_markup=kb_for_contact_or_back)

async def help_for_2(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Вывод золота происходит до 24 часов от запроса на вывод. Но в большинстве вывод происходит от нескольких секунд до часа.',reply_markup=kb_for_contact_or_back)

async def help_for_3(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Чеки проверяются в ручную, а не автоматически. Если вы пополнили рано утром или поздно вечером, то наши сотрудники не смогут проверить чек. Проверка чека занимает до 24 часов.',reply_markup=kb_for_contact_or_back)

async def help_for_4(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Если вы пополняли через QIWI, то найдите сообщение где вам выдали ссылку на оплату, и под этим сообщением будет кнопка «Проверить оплату» нажмите её. Но если вы пополняли другим способом, то вы, возможно, скинули боту чек файлом. В подобном случае, нажмите: "Пополнить баланс"; укажите сумму; "Другим способом"; " Отправить чек ". После, отправьте скриншот чека.',reply_markup=kb_for_contact_or_back)

async def help_for_5(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Весь товар, который продаётся в боте, получен честным путём. Если вы сомневаетесь в безопасности, то лучше покупать в игре.',reply_markup=kb_for_contact_or_back)

async def help_for_6(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Мы не покупаем товары других пользователей, так как, не знаем, откуда они их достали, а если знаем, это не является гарантией безопасности. Безопасность пользователей на первом месте для нас, и мы продаём только свои товары, в которых уверенны на 100%',reply_markup=kb_for_contact_or_back)

async def help_for_7(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Вывод золота занимает до 24 часов. Но мы стараемся как можно быстрее вывести вам золото. В большинстве случаев, есть очередь, и пока она дойдёт до вас, может пройти немного времени. Но если вы уже пол часа как на 1 месте, это может быть из-за проблем с рынком ( сложно искать скин) или работник взял перерыв.',reply_markup=kb_for_contact_or_back)		

async def help_for_back(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text_for_help,reply_markup=kb_for_help)


class tech_qvest(StatesGroup):
	qvest = State()
async def need_tech_help (callback:types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,'Напишите пожалуйста свой вопрос',reply_markup=kb_client_main_menu)
	await tech_qvest.qvest.set()

async def take_qvest (message:types.Message,state = FSMContext):
	if message.text!="Главное меню ⬅️":
		if db.support_exists(message.from_user.id):
			await state.finish()
			await bot.send_message(message.from_user.id,'У вас уже есть активный запрос в поддержку')
		else:
			db.add_support(message.from_user.id)
			qvest = str(message.text)
			chat_id = message.chat.id
			button_url = f'tg://user?id={chat_id}'
			markup = types.InlineKeyboardMarkup()
			markup.add(types.InlineKeyboardButton(text='Связаться', url=button_url),InlineKeyboardButton(text='Удалить его запрос',callback_data =f'del_support {message.from_user.id}'))
			await bot.send_message(admin_chat_id,qvest, reply_markup=markup)	
			await bot.send_message(message.from_user.id,'Ожидайте, вам ответят в ближайшее время')
			await state.finish()
	else:
		await state.finish()
		await commands_start(message)
		await bot.send_message(message.from_user.id,'Главное меню ⬅️')

async def del_support (callback:types.CallbackQuery):
	await callback.message.delete()
	id_user = callback['data'].replace('del_support ','')
	db.delete_support(id_user)
	await bot.send_message(admin_chat_id,'Запрос в поддержку был удален')
#######################ИНЛАЙН КНОПКИ ДЛЯ КЕЙСОВ##################################


async def nachalo(callback: types.CallbackQuery):
	await callback.message.delete()
	text = 'Содержимое кейса Начало:\n\nST Desert Eagle ‘Red Dragon’ - 20G\nST FAMAS ‘Beagle’ - 30G\nST AKR12 ‘Flow’ - 28G\nST AKR12 ‘Transistor’ 29 - 29G\nP90 ‘Ghoul’ - 30G\nP350 ‘Neon’ - 35G\nAKR12 ‘4 Years’ - 42G\nSticker ‘4 Years Color’ - 62G\nMP7 ‘Graffity’ - 30G'
	await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Открыть за 25 руб.',callback_data = "buy_nachalo_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_chest_")))

async def opit_chest(callback: types.CallbackQuery):
	text = 'Содержимое кейса Опытный:\n\nUMP45 ‘Cyberpunk’ - 37G\nCharm ‘Katana’ - 44G\nChibi ‘Crunch’ - 55G\nST  FabM ‘Parrot’ - 63G\nMP7 ‘Winter Sport’ - 60G\nST AWM ‘Polar Night - 71G\nMP7 ‘2 Years’ - 67G\nAKR ‘Necromancer’ - 83G\nP350 ‘Forest Spirit’ - 112G'
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Открыть за 50 руб.',callback_data = "buy_opit_chest_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_chest_")))

async def god_chest(callback: types.CallbackQuery):
	text = 'Содержимое кейса Бог:\n\nST AKR ‘Nano’ - 87G\nG22 ‘Monster’ - 99G\nP90 ‘Samurai’ - 121G\nCharm ‘Sale’ - 140G\nST F/S ‘Rush’ - 157G\nCase ‘Furious’ - 170G\nST AKR ‘Carbon’ - 118G\nM40 ‘Winter Track’ - 145G\nCharm ‘Cone’ - 200G'
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Открыть за 100 руб.',callback_data = "buy_god_chest_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_chest_")))

async def major_chest(callback: types.CallbackQuery):
	text = 'Содержимое кейса Мажор:\n\nP350 ‘Radiation’ - 444G\nMP7 ‘Blizzard’ - 500G\nCharm ‘Zen’ - 620G\nST AKR12 ‘Geometric’ - 650G\nAWM ‘Sport’ - 697G\nST P90 ‘Samurai’ - 710G\nFAMAS ‘Monster’ - 774G\nM4 ‘Samurai’ - 801G\nFlip ‘Snow Camo’ - 1020G'
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Открыть за 555 руб.',callback_data = "buy_major_chest_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_chest_")))

async def gold_chest(callback: types.CallbackQuery):
	text = 'Содержимое кейса Золотой:\n\nFN FAL ‘Phoenix Rise’ - 860G\nDeser Eagle ‘Yakuzą’ - 867G\nUSP ‘Geometric’ - 904G\nST FAMAS ‘Fury’ - 950G\nScorpion ‘Sea Yes’ - 1000G\nFlip ‘Frozen’ - 1123G\nKunai ‘Cold Flame’ - 1250G\nFlip ‘Vortex’ - 1297G\nKnife Tanto ‘Dojo’ - 1600G'
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text,reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Открыть за 777 руб.',callback_data = "buy_gold_chest_")).add(InlineKeyboardButton(text='Назад',callback_data = "back_to_chest_")))

def time_now():
	now = str(datetime.datetime.now())
	time = now.split('.')[0]
	time = time.replace('-','')
	time = time.replace(' ','')
	time = time.replace(':','')
	return time
def time_list_now(time_list):
	time = [time_list[0:4],time_list[4:6],time_list[6:8],time_list[8:10],time_list[10:12],time_list[12:14]]
	 ###########ГОД##########МЕСЯЦ###########ДЕНЬ##############ЧАС##########МИНУТА###########СЕКУНДА#######
	return time
def time_to_string(time):
	now = ''
	for i in range(6):
		now = now+str((time)[i])
	return now

###############################################ПОЛИНА ПИСЮН###############################

async def free_chest(callback: types.CallbackQuery):
	chest_time = db.user_free_chest(callback.from_user.id)
	if (len(str(chest_time)) == 3):
		free_gold_win = random.randint(1,5)
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+(free_gold_win))
		time = time_list_now(time_now())
		new_day=int(time[2])+3
		if new_day<10:
			new_day = '0'+str(new_day)
		new_day = str(new_day)
		time[2] = new_day
		db.set_free_chest(callback.from_user.id,str(time_to_string(time)))
		await callback.message.delete()
		await bot.send_message(callback.from_user.id,f'На ваш счет зачислено {free_gold_win}G')
	elif int(chest_time)<= int(time_now()):
		#print(int(chest_time))
		free_gold_win = random.randint(1,5)
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+(free_gold_win))
		time = time_list_now(time_now())
		new_day=int(time[2])+3
		if new_day<10:
			new_day = '0'+str(new_day)
		new_day = str(new_day)
		time[2] = new_day
		db.set_free_chest(callback.from_user.id,str(time_to_string(time)))
		await callback.message.delete()
		await bot.send_message(callback.from_user.id,f'На ваш счет зачислено {free_gold_win}G')		
	else:
		chest_time = time_list_now(str(chest_time))
		time = time_list_now(time_now())
		time_can = datetime.timedelta(days=int(time[2]),hours= int(time[3]), minutes=int(time[4]), seconds=int(time[5]))
		time_cur = datetime.timedelta(days = int(chest_time[2]),hours= int(chest_time[3]) , minutes=int(chest_time[4]), seconds=int(chest_time[5]))
		delta = time_cur - time_can
		delta = str(delta).split(' ')
		chours = delta[2].split(':')	
		count_hours = f'{chours[0]}:{chours[1]}:{chours[2]}'
		await callback.message.delete()
		await bot.send_message(callback.from_user.id,f'Вы уже открыли бесплатный кейс.\nСледующий кейс будет доступен через: {delta[0]} дней, {count_hours}')

async def back_to_chest(callback: types.CallbackQuery):
	await callback.message.delete()
	await chests(callback)


###############################ОТКРЫТИЕ КЕЙСОВ############################################
async def buy_nachalo(callback: types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 25:

		db.set_money(callback.from_user.id, user_money-25)
		can_win = ['ST Desert Eagle ‘Red Dragon’ - 20G','ST FAMAS ‘Beagle’ - 30G','ST AKR12 ‘Flow’ - 28G','ST AKR12 ‘Transistor’ 29 - 29G','P90 ‘Ghoul’ - 30G','P350 ‘Neon’ - 35G','AKR12 ‘4 Years’ - 42G','Sticker ‘4 Years Color’ - 62G','MP7 ‘Graffity’ - 30G']
		win = can_win[random.randint(0,len(can_win)-1)].split('-')
		await bot.send_message(callback.from_user.id,f"Поздравляем, вам выпало {win[0]} стоимостью {win[1]}.\nНа ваш счет зачислено {win[1].strip('G')} золота")
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+int(win[1].strip('G')))
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')

async def buy_opit_chest(callback: types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 50:

		db.set_money(callback.from_user.id, user_money-50)
		can_win = ['UMP45 ‘Cyberpunk’ - 37G','Charm ‘Katana’ - 44G','Chibi ‘Crunch’ - 55G','ST  FabM ‘Parrot’ - 63G','MP7 ‘Winter Sport’ - 60G','ST AWM ‘Polar Night - 71G','MP7 ‘2 Years’ - 67G','AKR ‘Necromancer’ - 83G','P350 ‘Forest Spirit’ - 112G']
		win = can_win[random.randint(0,len(can_win)-1)].split('-')
		await bot.send_message(callback.from_user.id,f"Поздравляем, вам выпало {win[0]} стоимостью {win[1]}.\nНа ваш счет зачислено {win[1].strip('G')} золота")
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+int(win[1].strip('G')))
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')

async def buy_god_chest(callback: types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 100:

		db.set_money(callback.from_user.id, user_money-100)
		can_win = ['ST AKR ‘Nano’ - 87G','G22 ‘Modnster’ - 99G','P90 ‘Samurai’ - 121G','Charm ‘Sale’ - 140G','ST F/S ‘Rush’ - 157G','Case ‘Furious’ - 170G','ST AKR ‘Carbon’ - 118G','M40 ‘Winter Track’ - 145G','Charm ‘Cone’ - 200G']
		win = can_win[random.randint(0,len(can_win)-1)].split('-')
		await bot.send_message(callback.from_user.id,f"Поздравляем, вам выпало {win[0]} стоимостью {win[1]}.\nНа ваш счет зачислено {win[1].strip('G')} золота")
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+int(win[1].strip('G')))
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')


async def buy_major_chest(callback: types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 555:

		db.set_money(callback.from_user.id, user_money-555)
		can_win = ['P350 ‘Radiation’ - 444G','MP7 ‘Blizzard’ - 500G','Charm ‘Zen’ - 620G','ST AKR12 ‘Geometric’ - 650G','AWM ‘Sport’ - 697G','ST P90 ‘Samurai’ - 710G','FAMAS ‘Monster’ - 774G','M4 ‘Samurai’ - 801G','Flip ‘Snow Camo’ - 1020G']
		win = can_win[random.randint(0,len(can_win)-1)].split('-')
		await bot.send_message(callback.from_user.id,f"Поздравляем, вам выпало {win[0]} стоимостью {win[1]}.\nНа ваш счет зачислено {win[1].strip('G')} золота")
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+int(win[1].strip('G')))
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')

async def buy_gold_chest(callback: types.CallbackQuery):
	user_money = db.user_money(callback.from_user.id)
	await callback.message.delete()
	if user_money >= 777:

		db.set_money(callback.from_user.id, user_money-777)
		can_win = ['FN FAL ‘Phoenix Rise’ - 860G','Deser Eagle ‘Yakuzą’ - 867G','USP ‘Geometric’ - 904G','ST FAMAS ‘Fury’ - 950G','Scorpion ‘Sea Yes’ - 1000G','Flip ‘Frozen’ - 1123G','Kunai ‘Cold Flame’ - 1250G','Flip ‘Vortex’ - 1297G','Knife Tanto ‘Dojo’ - 1600G']
		win = can_win[random.randint(0,len(can_win)-1)].split('-')
		await bot.send_message(callback.from_user.id,f"Поздравляем, вам выпало {win[0]} стоимостью {win[1]}.\nНа ваш счет зачислено {win[1].strip('G')} золота")
		user_gold = db.user_gold(callback.from_user.id)
		db.set_gold(callback.from_user.id, user_gold+int(win[1].strip('G')))
	else:
		await bot.send_message(callback.from_user.id,'На вашем счете недостаточно средств!')

async def help_for_back(callback: types.CallbackQuery):
	await callback.message.delete()
	await bot.send_message(callback.from_user.id,text_for_help,reply_markup=kb_for_help)

#######################ИНЛАЙН КНОПКИ ДЛЯ КЕЙСОВ##################################


async def check(callback: types.CallbackQuery):
	await callback.message.delete()
	bill = str(callback.data[6:])
	info = db.get_check(bill)
	if info != False:
		if str(p2p.check(bill_id=bill).status) =="PAID":
			user_money = db.user_money(callback.from_user.id)

			money = int(info[2])
			db.set_money(callback.from_user.id, user_money+money)
			await bot.send_message(callback.from_user.id,f"Успешная оплата!\nБаланс пополнен")
			db.delete_check(bill)
			id_referrer = db.user_referrer(callback.from_user.id)
			if id_referrer is not None:
				ref_gold = db.user_gold(id_referrer)
				db.set_gold(id_referrer,int(ref_gold)+5)
				await bot.send_message(id_referrer,"Вы получили 5 золота за покупку вашего реферала")
		else:
			await bot.send_message(callback.from_user.id,"Ваша транзакция не найдена!\nЕсли у вас возникла ошибка, обратитесь в поддержку",reply_markup=buy_menu(False,bill=bill))
	else:
		await bot.send_message(callback.from_user.id,"Счет не найден")

class vladd(StatesGroup):
	vlad = State()
async def send_vlad(message:types.Message):
	await bot.send_message(message.from_user.id,f'че сказать владу?')
	await vladd.vlad.set()
class Mos_shop(StatesGroup):
	shop = State()

async def Moscow_shop(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[6] == "Москва" or user_data[23] >= 1 :
		kb = ReplyKeyboardMarkup()\
		.add(KeyboardButton("Очки"))\
		.add(KeyboardButton("Майки"))\
		.add(KeyboardButton("Худи"))\
		.add(KeyboardButton("Главное меню ⬅️"))
		if user_data[23] == 1:
			await bot.send_message(message.from_user.id,'Твое следующее задание\nКупи себе любую вещь из магазина, чтобы получить награду')
		await bot.send_photo(message.from_user.id,open("skin/moscow_shop.jpg",'rb'),'Добро пожаловать в магазин "Gussi"!\nВыберете категорую одежды',reply_markup =kb)
		await Mos_shop.shop.set()
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")


async def pick_mos_shop (message:types.Message,state:FSMContext):
	if message.text != 'Главное меню ⬅️':
		if message.text == "Очки":
			await bot.send_message(message.from_user.id,'Добро пожаловать в раздел очков!\nТут мы можете выбрать очки на любой вкус!',reply_markup =types.ReplyKeyboardRemove())
			global position_glasses
			position_glasses = {message.from_user.id:0}
			await show_glasses(message,'glasses')
			await state.finish()
		elif message.text == "Майки":
			await bot.send_message(message.from_user.id,'Добро пожаловать в раздел маек!\nТут мы можете выбрать майки на любой вкус!',reply_markup =types.ReplyKeyboardRemove())
			global position_Tshirt
			position_Tshirt = {message.from_user.id:0}
			await show_glasses(message,'t-shirt')
			await state.finish()

		elif message.text == "Худи":
			await bot.send_message(message.from_user.id,'Добро пожаловать в раздел Худи!\nТут мы можете выбрать майки на любой вкус!',reply_markup =types.ReplyKeyboardRemove())
			global position_hoody
			position_hoody = {message.from_user.id:0}
			await show_glasses(message,'hoody')
			await state.finish()			
	else:
		await state.finish()
		await bot.send_message(message.from_user.id,'Главное меню ⬅️')
		await main_menu(message)



async def Barbershop_shop(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[6] == "Питер":
		global position_SPB_barbershop
		position_SPB_barbershop = {message.from_user.id:0}
		await bot.send_message(message.from_user.id,f'Добро пожаловать в парихмахерскую!Тут ты можешь выбарть себе прическу и поменять ее в любое время!')
		await show_glasses(message,'SPB_barbershop')
		if user_data[23] == 3:
			db.set_user_data(message.from_user.id,'can_home',1)
			db.set_user_data(message.from_user.id,'Level_task',4)								
			db.set_user_data(message.from_user.id,'gold',user_data[12]+500)
			await bot.send_message(message.from_user.id,'Молодец, ты выполнил задание!Можешь посмотреть, какие стрижки тебе достуины, либо выполнять задания дальше\n\nТвоя награда\n1.500 золота🥇\n2.Разблокированы дома\n3.Теперь можно посетить Сочи\n\nЗагляни в меню "Дом", чтобы получит следующее задание')
	else:
		await bot.send_message(message.from_user.id,"Этого нет в твоем городе, открой карту")


async def show_glasses(message,category):
	backround = None
	new_hair = None
	if category == "glasses":
		global position_glasses
		#files = [x for x in os.listdir(f'skin/shop/{category}') if category in x]#Ищем все нужные файлы
		files = db.items_base_data(category)
		#file = files[position_glasses[message.from_user.id]]

		if position_glasses[message.from_user.id] > len(files)-1 or position_glasses[message.from_user.id] < -(len(files)-1):#Нужно для того что бы можно было крутить по кругу
			position_glasses[message.from_user.id] = 0
		file = files[position_glasses[message.from_user.id]]
		#ph = open(f'skin/shop/{category}/{files[position_glasses[message.from_user.id]]}','rb')#Открываем нужную картинку

		ph = open(f'skin{file[1]}.png','rb')#Открываем нужную картинку

		#price =(files[position_glasses[message.from_user.id]].split('('))[1].split(')')[0]#Узнаем цену нужного товара
		price = file[3]

		#text = [f'"Стандартные очки"\nСтоимость:{price}G\n\nЕсли не хочется ходить с очками но денег нет, то это лучший выбор!',f'"Очки поблатнее"\nCтоимость:{price}G\nДля тех кто не на помойке себя нашел, но денег не много',f'"Очки для плавания"\nСтоимость:{price}G\nЧто бы шампунь в глаза не попал)',f'"Очки гуси"\nСтоимость:{price}G\nТупа стиль']#Описание каждого товара
		#text = file[5]

		#name = text[position_glasses[message.from_user.id]].split('\n')[0] 
		name = file[2]

		#directory_clothes = files[position_glasses[message.from_user.id]][:-4]#Узнаем путь нужного товара и срезаем .png
		directory_clothes = file[1]

		#text_clothes = text[position_glasses[message.from_user.id]]#Описание нужного товара
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'

		#new_glasses = f'shop/{category}/{directory_clothes}'#Фиксируем что у нас есть новые очки для картинки
		new_glasses = directory_clothes
		new_body = None #Фиксируем что нет новых худи

	elif category == 't-shirt':#Все тоже самое только для маек
		global position_Tshirt
		files = db.items_base_data(category)
		file = files[position_Tshirt[message.from_user.id]]
		if position_Tshirt[message.from_user.id] > len(files)-1 or position_Tshirt[message.from_user.id] < -(len(files)-1):
			position_Tshirt[message.from_user.id] = 0
		ph = open(f'skin{file[1]}.png','rb')
		price = file[3]
		name = file[2]
		directory_clothes = file[1]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = directory_clothes

	elif category == 'hoody':#Все тоже самое только для худи
		global position_hoody
		files = db.items_base_data(category)
		file = files[position_hoody[message.from_user.id]]
		if position_hoody[message.from_user.id] > len(files)-1 or position_hoody[message.from_user.id] < -(len(files)-1):
			position_hoody[message.from_user.id] = 0
		ph = open(f'skin{file[1]}.png','rb')
		price = file[3]
		name = file[2]	
		directory_clothes = file[1]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = directory_clothes


	elif category == 'SPB_barbershop':
		global position_SPB_barbershop
		files = db.items_base_data(category)
		file = files[position_SPB_barbershop[message.from_user.id]]
		if position_SPB_barbershop[message.from_user.id] > len(files)-1 or position_SPB_barbershop[message.from_user.id] < -(len(files)-1):
			position_SPB_barbershop[message.from_user.id] = 0
		ph = open(f'skin{file[1]}.png','rb')
		price = file[3]
		#text = [f'Хуйня',"12",'123']
		name = file[2]	
		directory_clothes = file[1]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = None
		new_hair  = directory_clothes

	elif category == 'home_Moscow':
		global position_home_Moscow
		#files = [x for x in os.listdir(f'skin/shop_home/{category}') if category in x]
		files = db.items_base_data(category)
		file = files[position_home_Moscow[message.from_user.id]]
		if position_home_Moscow[message.from_user.id] > len(files)-1 or position_home_Moscow[message.from_user.id] < -(len(files)-1):
			position_home_Moscow[message.from_user.id] = 0
		#ph = open(f'skin/shop_home/{category}/{files[position_home_Moscow[message.from_user.id]]}','rb')
		ph = open(f'skin{file[1]}.png','rb')
		#price =(files[position_home_Moscow[message.from_user.id]].split('('))[1].split(')')[0]
		price = file[3]
		#name = text[position_home_Moscow[message.from_user.id]].split('\n')[0]
		name = file[2]	
		#directory_clothes = files[position_home_Moscow[message.from_user.id]][:-4]
		directory_clothes = file[1]
		#text_clothes = text[position_home_Moscow[message.from_user.id]]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = None
		#backround  = f'shop_home/{category}/{directory_clothes}'
		backround = directory_clothes


	elif category == 'home_SPB':
		global position_home_SPB
		files = db.items_base_data(category)
		file = files[position_home_SPB[message.from_user.id]]	
		if position_home_SPB[message.from_user.id] > len(files)-1 or position_home_SPB[message.from_user.id] < -(len(files)-1):
			position_home_SPB[message.from_user.id] = 0
		ph = open(f'skin{file[1]}.png','rb')
		price = file[3]
		name = file[2]	
		directory_clothes = file[1]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = None
		backround = directory_clothes

	elif category == 'home_Sochi':
		global position_home_Sochi
		files = db.items_base_data(category)
		file = files[position_home_Sochi[message.from_user.id]]
		if position_home_Sochi[message.from_user.id] > len(files)-1 or position_home_Sochi[message.from_user.id] < -(len(files)-1):
			position_home_Sochi[message.from_user.id] = 0
		ph = open(f'skin{file[1]}.png','rb')
		price = file[3]
		name = file[2]	
		directory_clothes = file[1]
		text_clothes = f'{name}\nСтоимость: {price}G\n{file[5]}'
		new_glasses = None
		new_body = None
		backround = directory_clothes		
	kb = InlineKeyboardMarkup().row(InlineKeyboardButton('⬅',callback_data = f'scroll_clothes_ back {category}')\
		,InlineKeyboardButton('Купить',callback_data =f'buy_clothes {category},{name},{price}')\
		,InlineKeyboardButton('➡',callback_data = f'scroll_clothes_ next {category}'))\
	.add(InlineKeyboardButton('Назад',callback_data = f'exit_clothes_type {category}'))
	#new_glasses = f'shop/{category}/{directory_clothes}
	await bot.send_photo(message.from_user.id,charecter_img(message.from_user.id,new_glasses = new_glasses,new_body = new_body,backround = backround,new_hair = new_hair),text_clothes,reply_markup = kb)

async def scroll_clothes(callback:types.CallbackQuery):
	data = (((callback['data'].replace('scroll_clothes_ ','')).split()))
	way,type_clothes= data[0],data[1]
	if type_clothes == 'glasses':
		global position_glasses
		if way == 'next':
			position_glasses[callback.from_user.id] += 1
		elif way == 'back':
			position_glasses[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'glasses')
	elif type_clothes == 't-shirt':
		global position_Tshirt
		if way == 'next':
			position_Tshirt[callback.from_user.id] += 1
		elif way == 'back':
			position_Tshirt[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 't-shirt')

	elif type_clothes == 'hoody':
		global position_hoody
		if way == 'next':
			position_hoody[callback.from_user.id] += 1
		elif way == 'back':
			position_hoody[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'hoody')

	elif type_clothes == 'SPB_barbershop':
		global position_SPB_barbershop
		if way == 'next':
			position_SPB_barbershop[callback.from_user.id] += 1
		elif way == 'back':
			position_SPB_barbershop[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'SPB_barbershop')

	elif type_clothes == 'home_Moscow':
		global position_home_Moscow
		if way == 'next':
			position_home_Moscow[callback.from_user.id] += 1
		elif way == 'back':
			position_home_Moscow[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'home_Moscow')

	elif type_clothes == 'home_SPB':
		global position_home_SPB
		if way == 'next':
			position_home_SPB[callback.from_user.id] += 1
		elif way == 'back':
			position_home_SPB[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'home_SPB')

	elif type_clothes == 'home_Sochi':
		global position_home_Sochi
		if way == 'next':
			position_home_Sochi[callback.from_user.id] += 1
		elif way == 'back':
			position_home_Sochi[callback.from_user.id] -= 1
		await callback.message.delete()
		await show_glasses(callback,category = 'home_Sochi')
async def buy_clothes(callback:types.CallbackQuery):
	await callback.message.delete()
	data = (callback['data'].replace('buy_clothes ','')).split(',')
	user_data = db.about_user(callback.from_user.id)
	category,name,price = data
	if category == 'glasses':
		data_pos = 14

	elif category == 'SPB_barbershop':
		data_pos = 4
	elif category in ['t-shirt','hoody']:
		data_pos = 13
	elif 'home' in category:
		if 'Moscow' in category:
			data_pos = 20
		elif 'SPB' in category:
			data_pos = 21
		elif 'Sochi' in category:
			data_pos = 22

	cur_item = user_data[0][data_pos]
	if cur_item == None or data_pos == 4:#Проверяем есть ли у нас в этом слоте что то
		text_msg = f'Вы уверены что хотите купить {name}\nЗа {price}G?'
		cur_item_price = 0
	elif data_pos in [14,13]:#Если это одежда
		cur_item_price =(cur_item.split('('))[1].split(')')[0]
		cur_item_price = round(int(cur_item_price)/2)
		text_msg = f'Вы уверены что хотите купить {name}\nЗа {price}G?\nВНИМАНИЕ\nНа вас уже надета похожая одежда, после подтверждения покупки она будет продана за 50% от совей цены!\nВы продадите текущую вещь за {cur_item_price}G'
	elif data_pos in [20,21,22] :#Если это дом
		cur_item_price =(cur_item.split('('))[1].split(')')[0]
		cur_item_price = round(int(cur_item_price)/2)
		my_town = user_data[6]
		#####################
		if my_town == 'Москва':#Меняем переменную на английский в зависимости от того какой город
			my_town = 'Moscow'
		if my_town == 'Питер':
			my_town = 'SPB'
		if my_town == 'Сочи':
			my_town = 'Sochi'
		#####################	
		if my_town in cur_item:
			#if my_town in cur_item:
			text_msg = f'Вы уверены что хотите купить {name}\nЗа {price}G?\nВНИМАНИЕ\nУ вас уже есть дом в этом городе, после подтверждения покупки он будет продан за 50% от совей цены!\nВы продадите его за {cur_item_price}G'		
			#else:
			#	text_msg = f'Вы уверены что хотите купить {name}\nЗа {price}G?'
			#	cur_item_price = 0
		else:
			await bot.send_message (callback.from_user.id,'Этого нет в твоем городе')	
	await bot.send_message(callback.from_user.id,text_msg,reply_markup =InlineKeyboardMarkup()\
		.add(InlineKeyboardButton(text = 'Подтвердить покупку',callback_data = f'apply_bay_clothes {category},{name},{price}'))\
		.add(InlineKeyboardButton(text = 'Отмена',callback_data = f'cancel_bay_clothes {category}')))

async def apply_bay_clothes(callback:types.CallbackQuery):
	await callback.message.delete()
	data = (callback['data'].replace('apply_bay_clothes ','')).split(',')
	category,name,price = data
	slot = category
	user_data = db.about_user(callback.from_user.id)[0]
	if 'home' in category:
		dir_bay = 'shop_home'
	elif category =='SPB_barbershop':
		dir_bay = 'barbershop'
	else:
		dir_bay = 'shop'
	user_gold = db.user_gold(callback.from_user.id)
	files = db.items_base_data(category)
	if user_gold>=int(price):
		if category == 'glasses':
			global position_glasses
			data_pos = 14
			pos_file = position_glasses[callback.from_user.id]

		elif category == 'SPB_barbershop':
			global position_SPB_barbershop
			data_pos = 4
			pos_file = position_SPB_barbershop[callback.from_user.id]
			slot = 'hairstyle'
		elif category in ['t-shirt','hoody']:
			slot = 'body'
			data_pos = 13
			if category == 't-shirt':
				global position_Tshirt
				pos_file = position_Tshirt[callback.from_user.id]
			else:
				global position_hoody
				pos_file = position_hoody[callback.from_user.id]
		elif 'home' in category:
			slot = category
			if 'Moscow' in category:
				global position_home_Moscow
				pos_file = position_home_Moscow[callback.from_user.id]				
				data_pos = 20
			elif 'SPB' in category:
				global position_home_SPB
				pos_file = position_home_SPB[callback.from_user.id]	
				data_pos = 21
			elif 'Sochi' in category:
				global position_home_Sochi
				pos_file = position_home_Sochi[callback.from_user.id]	
				data_pos = 22
		if category != 'SPB_barbershop':
			cur_item = user_data[data_pos]
			if cur_item != None:
				cur_item_price =(cur_item.split('('))[1].split(')')[0]
				cur_item_price = int(cur_item_price)/2
				db.set_gold(callback.from_user.id, user_gold+int(cur_item_price))#даем деньги за старую вещь если есть
		db.set_user_data(callback.from_user.id,slot,files[pos_file][1][1:])#Отдаем вещь
		db.set_gold(callback.from_user.id, user_gold-int(price))#берем плату за вещь
		await bot.send_message(callback.from_user.id,f"Вы успешно купили {name}\nС вашего счета списано {price}G!\nСпасибо за покупку!")
		if user_data[23] == 1:
			db.set_user_data(callback.from_user.id,'Level_task',2)
			db.set_user_data(callback.from_user.id,'gold',(user_gold-int(price))+1000)
			db.set_user_data(callback.from_user.id,'can_job',2)
			await bot.send_message(callback.from_user.id,"Поздравляю, ты выполнил второе задание!\nТвоя награда\n1. 1000 золота🥇\n2.Разблокирована новая работа!\n\nПоработай на новой работе, чтобы получить следующее задание")

		await show_glasses(callback,category)
	else:
		await bot.send_message(callback.from_user.id,f"У вас недостаточно золота(\nВам не хватает {int(price)-user_gold} G")
		await show_glasses(callback,category)


async def cancel_bay_clothes(callback:types.CallbackQuery):
	await callback.message.delete()
	data = callback['data'].replace('cancel_bay_clothes ','')
	if 'home' in data:
		await commands_start(callback)
	else:
		await show_glasses(callback,category = data)



async def exit_clothes_type(callback:types.CallbackQuery):
	data = callback['data'].replace("exit_clothes_type ",'')
	await callback.message.delete()
	if data in ['glasses','t-shirt','hoody']:
		await Moscow_shop(callback)
	elif 'home' in data or data == 'SPB_barbershop':
		await commands_start(callback)

	if data == 'glasses':#Проверяем из какого раздела выходим
		global position_glasses
		poz_item = position_glasses
	elif data == 't-shirt':
		global position_Tshirt
		poz_item = position_Tshirt
	elif data == 'hoody':
		global position_hoody
		poz_item = position_hoody
	elif data == 'SBP_barbershop':
		global position_SBP_barbershop
		poz_item = position_SBP_barbershop
	elif data == 'home_Moscow':
		global position_home_Moscow
		poz_item = position_home_Moscow
	elif data == 'home_SPB':		
		global position_home_SPB
		poz_item = position_home_SPB
	elif data == 'home_Sochi':		
		global position_home_Sochi
		poz_item = position_home_Sochi
	try:#Пытаемся удалить уже не нужную переменную(счетчик позиции)
		del poz_item[callback.from_user.id]
	except:
		pass

class home_menu_button(StatesGroup):
	button = State()

async def home_menu(message:types.Message):
	user_data = db.about_user(message.from_user.id)[0]
	if user_data[6] == 'Москва' or user_data[6] == 0 :
		home_slot = 20
	elif user_data[6] == 'Питер':
		home_slot = 21
	elif user_data[6] == 'Сочи':
		home_slot = 22
	#Проверили где находится игрок что бы проверить слот дома в этом городе

	if user_data[7] == 0:#Проверяем доступна ли эта функция игроку и заходит ли он сюда впервые
		await bot.send_message(message.from_user.id,'Тебе это еще не доступно!')
	elif user_data[7] == 1:
		await bot.send_message(message.from_user.id,f'🏠{user_data[1]} поздравляют тебя!Теперь тебе доступны дома!Тут ты можешь отдыхать и хранить вещи в шкафу!\nНажми еще раз на кнопку "Дом 🏠" что бы попасть в меню домов')
		db.set_user_data(message.from_user.id,'can_home',None)
		db.set_user_data(message.from_user.id,'Level_task',5)	
	elif user_data[home_slot] == None:#Проверяем есть ли в этом городе дом и если нет предлагаем купить
		text = 'У тебя еще нет дома в этом городе, вот дома которые можешь купить в этом городе'
		if user_data[23] == 5:
			text+='\nМожешь выбрать себе какой-нибудь, либо выйти в главное меню, там для тебя новое задание'
		await bot.send_message(message.from_user.id,text)
		if user_data[6] == 'Москва':
			global position_home_Moscow
			position_home_Moscow = {message.from_user.id:0}
			town = 'home_Moscow'
		elif user_data[6] == 'Питер':
			global position_home_SPB
			position_home_SPB = {message.from_user.id:0}
			town = 'home_SPB'
		elif user_data[6] == 'Сочи':
			global position_home_Sochi
			position_home_Sochi = {message.from_user.id:0}
			town = 'home_Sochi'	
		await show_glasses(message, town)
	else:
		home_name = (user_data[home_slot].split('/')[-1]).split('_')[0]
		kb = ReplyKeyboardMarkup(resize_keyboard=True)\
		.row(KeyboardButton("Гардероб"))\
		.row(KeyboardButton("Выйти"),KeyboardButton("Купить дом"))
		await home_menu_button.button.set()
		await bot.send_photo(message.from_user.id,charecter_img(message.from_user.id, backround = user_data[home_slot]),f'{user_data[1]}, ты сейчас находишься в своем доме "{home_name}"',reply_markup = kb)

class chenge_wardrobe_state(StatesGroup):
	chenge = State()
async def wardrobe(message:types.Message):
	user_data =db.about_user(message.from_user.id)[0]
	if db.wardrobe_exists(message.from_user.id):
		user_wardrobe = db.about_user_wardrobe(message.from_user.id)[0]
		new_glasses = 'None'	#Ставим значение очков на манекене изночально пустое
		new_body = 'None'
		body_in_slot = 'Пусто'
		skin = 'wardrobe_glasses' # Аналагично с верхней одеждо, названием верхней одежды и типом манекена
		kb = ReplyKeyboardMarkup(resize_keyboard=True)#Создаем клавиатуру пока что с одной кнопкой
		if user_data[6] =="Москва":#Узнаем в каком городе персонаж что бы показать именно этот фон
			back_poz = 20
		elif user_data[6] =="Питер":
			back_poz = 21
		elif user_data[6] == "Сочи":
			back_poz = 22

		if user_wardrobe[2] == None:#Если в слоте одежды пусто
			kb.row(KeyboardButton('Положить одежду👕'))
		elif user_wardrobe[2] != None:
			new_body = user_wardrobe[2]
			body_in_slot = db.items_dir_to_name(user_wardrobe[2])
			kb.row(KeyboardButton('Забрать одежду👕')) 
			
		if user_wardrobe[3] == 0:#Узнаем открыт ли раздел очков
			new_glasses = 'None'
			glasses_in_slot = '🔒ЗАБЛОКИРОВАНО🔒'
			skin = 'wardrobe_body'
			kb.insert(KeyboardButton('🔒РАЗБЛОКИРОВАТЬ СЛОТ ДЛЯ ОЧКОВ🔒'))
		elif user_wardrobe[3] == None:#Если раздел есть но там ничего нет
			kb.insert(KeyboardButton('Положить очки👓'))#Добовляем кнопку
			glasses_in_slot = 'Пусто'
		else:#Если стоят какие то очки
			kb.insert(KeyboardButton('Забрать очки👓'))#Добовляем кнопку
			new_glasses = user_wardrobe[3]
			glasses_in_slot = db.items_dir_to_name(user_wardrobe[3])
		kb.add(KeyboardButton('Назад'))
		wardrobe_ph = charecter_img(message.from_user.id,skin = skin, backround = user_data[back_poz],new_body = new_body,new_hair = 'None',new_glasses = new_glasses)#Создаем фото манекена
		await bot.send_photo(message.from_user.id,wardrobe_ph,f'Это твой гардероб\n👕Верхняя одежда:{body_in_slot}\n👓Очки:{glasses_in_slot}',reply_markup = kb)
		await chenge_wardrobe_state.chenge.set()
	else:
		kb = InlineKeyboardMarkup()\
		.row(InlineKeyboardButton(text = 'Купить', callback_data = 'bay_wardrobe body'),InlineKeyboardButton(text ='Главное меню',callback_data = 'back_main_menu'))
		await bot.send_message(message.from_user.id,f'{user_data[1]},у тебя еще нет гардероба,хочешь купить его за 200 000 G?\nВ нем уже будет слот для верхней одежды, но слот для очков нужно докупать отдельно',reply_markup = kb)	

async def chenge_wardrobe(message:types.Message,state:FSMContext):
	user_wardrobe = db.about_user_wardrobe(message.from_user.id)[0]
	user_data = db.about_user(message.from_user.id)[0]
	if message.text == 'Назад':
		await state.finish()
		await home_menu(message)
	elif message.text in ('Положить одежду👕','Забрать одежду👕'):
		if message.text == 'Положить одежду👕':
			db.set_user_data(message.from_user.id,'body',None)
			db.set_user_wardrobe(message.from_user.id,'body',user_data[13])
			await bot.send_message(message.from_user.id,'👕Вы положили свою одежду в гардероб')
		elif message.text == 'Забрать одежду👕':
			db.set_user_data(message.from_user.id,'body',user_wardrobe[2])
			db.set_user_wardrobe(message.from_user.id,'body',user_data[13])			
			await bot.send_message(message.from_user.id,'👕Вы забрали одежду из гардероба')
		await wardrobe(message)
		#await state.finish()


	elif message.text in('Положить очки👓','Забрать очки👓'):
		if user_wardrobe[3]==0:
			await bot.send_message(message.from_user.id,'Вам это еще не доступно!')
		elif message.text == 'Положить очки👓':
			db.set_user_data(message.from_user.id,'glasses',None)
			db.set_user_wardrobe(message.from_user.id,'glasses',user_data[14])
			await bot.send_message(message.from_user.id,'Вы положили свои очки в гардероб')
		elif message.text == 'Забрать очки👓':
			db.set_user_data(message.from_user.id,'glasses',user_wardrobe[3])
			db.set_user_wardrobe(message.from_user.id,'glasses',user_data[14])		
			await bot.send_message(message.from_user.id,'Вы забрали очки из гардероба')
		await wardrobe(message)
		#await state.finish()
	elif message.text == '🔒РАЗБЛОКИРОВАТЬ СЛОТ ДЛЯ ОЧКОВ🔒':
		await bay_wardrobe_glasses(message)
		await state.finish()
	else:
		await bot.send_message(message.from_user.id,'Используй кнопки!')

async def bay_wardrobe(callback:types.CallbackQuery):
	await callback.message.delete()
	user_data =db.about_user(callback.from_user.id)[0]
	if db.wardrobe_exists(callback.from_user.id):
		await bot.send_message(callback.from_user.id,f'{user_data[1]}, у тебя уже есть гардероб!')
		await commands_start(callback.from_user.id)
	else:
		kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text = 'Подтвердить',callback_data = 'apply_bay_wardrobe body'),InlineKeyboardButton(text = 'Отмена',callback_data = 'back_main_menu'))
		await bot.send_message(callback.from_user.id,f'{user_data[1]}, вы уверены что хотите купить гардероб за 200 000G?',reply_markup = kb)
	

async def bay_wardrobe_glasses(message:types.Message):
	user_data =db.about_user(message.from_user.id)[0]
	user_wardrobe = db.about_user_wardrobe(message.from_user.id)[0]
	if user_wardrobe[3]==0:
		kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text = 'Подтвердить',callback_data = 'apply_bay_wardrobe glasses'),InlineKeyboardButton(text = 'Отмена',callback_data = 'back_main_menu'))
		await bot.send_message(message.from_user.id,f'{user_data[1]}, вы уверены что хотите разблокировать слот для очков за 500 000G?',reply_markup = kb)			
	else:
		await bot.send_message(message.from_user.id,f'{user_data[1]}, у тебя уже открыт слот для очков!')
		await commands_start(message.from_user.id)





async def apply_bay_wardrobe(callback:types.CallbackQuery):
	await callback.message.delete()
	user_data =db.about_user(callback.from_user.id)[0]
	if 'body' in callback['data']:
		if user_data[12] >= 200000:
			db.create_wardrobe(callback.from_user.id)
			db.set_gold(callback.from_user.id,user_data[12]-200000)
			wardrobe_ph = open("skin/wardrobe_body.png",'rb')
			await bot.send_photo(callback.from_user.id,wardrobe_ph,f'Поздравляю {user_data[1]}, ты купил гардероб, и тебе уже доступен слот для верхней одежды\nЭтот гардероб ты можешь использовать в любом доме, любого города!\nОдну шмотку ты можешь носить на себе а другую хранить в шкафу!)')
			await home_menu(callback)
		else:
			await bot.send_message(callback.from_user.id,'У вас недостаточно золота!')
			await home_menu(callback)
	elif 'glasses' in callback['data']:
		if user_data[12] >= 500000:
			db.set_user_wardrobe(callback.from_user.id,'glasses',None)
			db.set_gold(callback.from_user.id,user_data[12]-500000)
			wardrobe_ph = open("skin/wardrobe_glasses.png",'rb')
			await bot.send_photo(callback.from_user.id,wardrobe_ph,f'Поздравляю {user_data[1]}, ты разблокировал слот для очков!')
			await home_menu(callback)
		else:
			await bot.send_message(callback.from_user.id,'У вас недостаточно золота!')
			await home_menu(callback)


async def back_main_menu_callback(callback:types.CallbackQuery):
	await callback.message.delete()
	await commands_start(callback)

async def home_buttons(message:types.Message,state:FSMContext):
	if message.text == "Выйти":
		await state.finish()
		await commands_start(message)
	else:
		if message.text == "Гардероб":
			await state.finish()
			await wardrobe(message)
		elif message.text == "Купить дом":
			await state.finish()
			user_data = db.about_user(message.from_user.id)[0]
			if user_data[6] == 'Москва':#Узнаем в каком городе сейчас игрок и создаем словать позиции товаров в магазине для нужного города, затем переходим в каталог домов в этом городе
				global position_home_Moscow
				position_home_Moscow = {message.from_user.id:0}
				town = 'home_Moscow'
			elif user_data[6] == 'Питер':
				global position_home_SPB
				position_home_SPB = {message.from_user.id:0}
				town = 'home_SPB'
			elif user_data[6] == 'Сочи':
				global position_home_Sochi
				position_home_Sochi = {message.from_user.id:0}
				town = 'home_Sochi'
			await bot.send_message(message.from_user.id,'Вот список домов в твоем городе которые ты можешь купить',reply_markup =types.ReplyKeyboardRemove())
			await show_glasses(message, town)
		else:
			await bot.send_message(message.from_user.id,'Используй кнопки!')


class bussines_menu_FSM(StatesGroup):
	menu = State()
	storage = State()
	catalog = State(0)

async def bussines(message:types.Message,state:FSMContext):
	user_data = db.about_user(message.from_user.id)[0]
	user_bussines = user_data[8]
	if user_bussines == 0:
		await bot.send_message(message.from_user.id,"Это тебе еще не доступно")
	elif user_bussines == 1:
		await bot.send_message(message.from_user.id,"У тебя пока нет бизнеса.Давай выберем тебе какой-нибудь")
		await bussines_menu_FSM.catalog.set()
		async with state.proxy() as data:
			data['catalog'] = 0
		await bussines_catalog(message,state)			
	elif user_bussines != 1:
		bussines_data = db.bussiness_data(user_bussines)#Читаем информацию из базы, описание бизнесса который у пользователя
		bussines_processes = db.business_processes(message.from_user.id)# За тем информацию о работе этого бизнесса

		start_time =datetime.datetime.strptime(bussines_processes["start_time"], "%Y-%m-%d %H:%M:%S.%f")#Считываем время начала работы
		now = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")#Время сейчас
		em_t = datetime.datetime.strptime(bussines_processes['storage_empty_time'], "%Y-%m-%d %H:%M:%S.%f")#Когда закончатся материалы
		delta_to_empty = (em_t-start_time).total_seconds() #Максимальное время, которое может проработать бизнесс
			
		if now > em_t : #Проверяем, осталось ли еще что то в хранилище, если не осталось, то бизнесс проработал максимум времени, сколько мог
			if delta_to_empty < 0:
				delta = 0
			else:
				delta = delta_to_empty
			cur_storage = 0

		elif start_time < now < em_t:#Если же осталось, то узнаем сколько времени проработал, от закупки материалом до данного момента
			delta = int((now-start_time).total_seconds())
			cur_storage = (((bussines_processes["storage"]*60) - delta)/60) #Считаем сколько должно остаться материалов в хранилище
			if cur_storage < 0:
				cur_storage = 0

		net_income = round((delta*bussines_data["net_income"])/60) #Чистая прибыль
		on_account = bussines_processes["on_account"] + net_income #На счету

		if bussines_processes['storage'] > 0:
			##########Заносим изменения в базу данных, если есть смысл#############
			#db.set_business_p_data(message.from_user.id,"storage_empty_time",datetime.datetime.now()+datetime.timedelta(minutes =bussines_processes["storage"] ))
			db.set_business_p_data(message.from_user.id,"storage",cur_storage)
			db.set_business_p_data(message.from_user.id,"on_account",on_account)
			if now < em_t:
				db.set_business_p_data(message.from_user.id,"start_time",now)
		else:
			on_account = bussines_processes["on_account"] #Если изменений не внесли
		#Далее делаем текст, который отправится в сообщении
		bussines_text = f'{user_data[1]},ты в меню управления своим бизнесом \n"{user_bussines}".\n💵 Счет бизнеса:${on_account}\n💸 Выручка:{bussines_data["income"]}$/мин.\n📈 Доход: {bussines_data["net_income"]}$/мин.\n📦 Склад: {math.ceil(cur_storage)}/{bussines_data["storage"]}'			
		if cur_storage <= 0:
			bussines_text += ('\nБизнесс на данный момент не работает, закупите материалов на склад!')
		kb = ReplyKeyboardMarkup(resize_keyboard = True)\
		.row(KeyboardButton("Обновить"),KeyboardButton("Снять со счета"),KeyboardButton("Пополнить склад"),KeyboardButton("Каталог"))\
		.add(KeyboardButton("Назад"))

		await bussines_menu_FSM.menu.set()
		with open(f'skin/business/{bussines_data["picture_dir"]}','rb') as picture:
			await bot.send_photo(message.from_user.id,picture,bussines_text,reply_markup = kb)
	else:
		await bot.send_message(message.from_user.id,f'{user_data[1]}, ты в меню бизнессов!\nПока что у тебя нет своего бизнеса, давай посмотрим, какие бизнессы ты можешь купить!')


count_b_cata = -1
async def bussines_menu(message:types.Message,state:FSMContext):
	if message.text == "Обновить":
		await bussines(message,state)

	elif message.text == "Назад":
		await commands_start(message)
		await state.finish()

	elif message.text in ("Снять со счета","Пополнить склад"):
		user_data = db.about_user(message.from_user.id)[0]
		b_account_data = db.business_processes(message.from_user.id)
		if message.text == "Снять со счета":
			user_data = db.about_user(message.from_user.id)[0]
			b_account_data = db.business_processes(message.from_user.id)
			db.set_user_data(message.from_user.id,"gold",user_data[12]+b_account_data["on_account"])
			db.set_business_p_data(message.from_user.id,"on_account",0)	
			await bot.send_message(message.from_user.id,f"Вы сняли со счета бизнеса {b_account_data['on_account']}🥇")
			await bussines(message,state)
		elif message.text == "Пополнить склад":
			b_data = db.bussiness_data(user_data[8])
			free_place = b_data["storage"] - math.ceil(b_account_data["storage"])
			if free_place > 0:
				await state.finish()
				await bussines_menu_FSM.storage.set()
				kb = ReplyKeyboardMarkup(resize_keyboard = True)\
				.row(KeyboardButton("Подтвердить"),KeyboardButton("Назад"))
				price = math.ceil(free_place*(b_data["net_income"]**0.5*2))
				async with state.proxy() as data:
					data['storage'] = price,user_data,b_account_data,b_data,free_place
				await bot.send_message(message.from_user.id,f'На складе вашего бизнеса поместится еще {free_place} материалов, заполнить весь склад за {price}',reply_markup = kb)
			else:
				await bot.send_message(message.from_user.id,f'На складе нет свободного места')
	elif message.text == "Каталог":
		await bot.send_message(message.from_user.id,"Добро пожаловать в каталог.Тут все бизнесы которые вы можете купить!\nДавайте выберем что-нибудь)")
		await state.finish()
		await bussines_menu_FSM.catalog.set()
		async with state.proxy() as data:
			data['catalog'] = 0
		await bussines_catalog(message,state)

	else:
		await bot.send_message(message.from_user.id,'Используй кнопки!')

async def bussines_catalog(message:types.Message,state = FSMContext):
	catalog = db.bussiness_data()
	async with state.proxy() as data:
		page = data['catalog']
		if page>=len(catalog) or page <= -len(catalog):
			data['catalog'] = page = 0 

	catalog = catalog[page]
	offer ={'bussines_id':catalog[0],'bussines_name':catalog[1],'income':catalog[2],'net_income':catalog[3],'storage':catalog[4],'description':catalog[5],'picture_dir':catalog[6],'price':catalog[7]}
	offer_text = f"{offer['bussines_name']}\nВыручка:{offer['income']}\nДоход:{offer['net_income']}\nВместимость склада:{offer['storage']}\nОписание:{offer['description']}\n\nЦена:{offer['price']}🥇"

	kb = ReplyKeyboardMarkup(resize_keyboard = True)\
	.row(KeyboardButton('⬅️'),KeyboardButton('Купить'),KeyboardButton('➡️'))\
	.add(KeyboardButton('Назад'))
	with open(f'skin/business/{offer["picture_dir"]}','rb') as picture:
		await bot.send_photo(message.from_user.id,picture,offer_text,reply_markup = kb)

async def bussines_catalog_way(message:types.Message,state = FSMContext):
	user_data = db.about_user(message.from_user.id)[0]

	if message.text == '➡️':
		async with state.proxy() as data:
			data['catalog']+=1
		await bussines_catalog(message,state)
	elif message.text == '⬅️':
		async with state.proxy() as data:
			data['catalog']-=1
		await bussines_catalog(message,state)
	elif message.text == 'Назад':
		await state.finish()
		if user_data[8] == 1: #Если перешел с главного меню, туда и возвращается
			await commands_start(message)
 
		else:
			await bussines(message,state)
			
	elif message.text == 'Купить':
		async with state.proxy() as data:
			page = data['catalog']
		cur_business = db.bussiness_data()[page]
		if user_data[12] >= cur_business[7]:
			if user_data[8] == 1:
				db.create_business_p(message.from_user.id)
			db.set_business_p_data(message.from_user.id,'bussines_name',cur_business[1])
			db.set_business_p_data(message.from_user.id,'start_time',datetime.datetime.now())
			db.set_business_p_data(message.from_user.id,'storage_empty_time',datetime.datetime.now())
			db.set_business_p_data(message.from_user.id,'on_account',0)
			db.set_business_p_data(message.from_user.id,'storage',0)
			db.set_user_data(message.from_user.id,'can_bussines',cur_business[1])
			db.set_user_data(message.from_user.id,'gold',user_data[12]-int(cur_business[7]))
			await bot.send_message(message.from_user.id,f'C вашего счета списанно {cur_business[7]} золота🥇\nПоздравляем вас с покупкой бизнеса "{cur_business[1]}"!\nВам осталось пополнить склад вашего нового бизнеса, и он начнет приносить прибыль!')
			await state.finish()
			await bussines(message,state)
		else:
			await bot.send_message(message.from_user.id,'У вас недостаточно золота на счету')


async def bussines_storage(message:types.Message,state:FSMContext):
	if message.text == "Подтвердить":
		async with state.proxy() as data:
			price,user_data,b_account_data,b_data,free_place = data['storage']
			if user_data[12] >= price:
				now = datetime.datetime.now()
				db.set_user_data(message.from_user.id,"gold",user_data[12]-price)
				db.set_business_p_data(message.from_user.id,"storage",b_data["storage"])
				
				if now > datetime.datetime.strptime(b_account_data['storage_empty_time'], "%Y-%m-%d %H:%M:%S.%f"):
					db.set_business_p_data(message.from_user.id,"start_time", now)		
					db.set_business_p_data(message.from_user.id,"storage_empty_time",now+datetime.timedelta(minutes =b_data["storage"] ))
				else:
					db.set_business_p_data(message.from_user.id,"storage_empty_time",now+datetime.timedelta(minutes =free_place ))

				await bot.send_message(message.from_user.id,f'Вы успешно заполнили заполнили склад материалами, с вашего счета списанно {price} золота')
			else:
				await bot.send_message(message.from_user.id,f'У вас недостаточно золота')
			await state.finish()
			await bussines(message,state)
	elif message.text == "Назад":
		await state.finish()
		await bussines(message,state)
	else:
		await bot.send_message(message.from_user.id,"Используй кнопки")





async def send_vladu(message:types.Message,state: FSMContext):
	await bot.send_message(812157716,message.text)
	await bot.send_message(message.from_user.id,f'Влад получил сообщение')

on_my_neck = 0

async def test_edit_button(message:types.Message):
	global on_my_neck
	#msg = await bot.send_message(message.from_user.id,f"У тебя на счету {on_my_neck}")

	await bot.send_message(message.from_user.id,f"У тебя на счету {on_my_neck}\nНажми на кнопку что бы получить еще",reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text = "Нажми на меня",callback_data = f"testEdit ")))
	
async def test_edit_button_callback(callback:types.CallbackQuery):
	global on_my_neck
	on_my_neck +=1
	await bot.edit_message_text(text = f"У тебя на счету {on_my_neck}\nНажми на кнопку что бы получить еще",chat_id = callback.message.chat.id ,message_id = callback.message.message_id,reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text = "Нажми на меня",callback_data = f"testEdit ")))

def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(commands_start,commands=['start','help'])
	dp.register_message_handler(add_new_key,commands=['add_key_PASSWORD'])

	dp.register_message_handler(test_edit_button,Text(equals='Тестим хуйню'))
	dp.register_callback_query_handler(test_edit_button_callback,lambda x: x.data and x.data.startswith('testEdit '))


	dp.register_message_handler(main_menu,Text(equals='Главное меню ⬅️'))
	dp.register_message_handler(up_balance, Text(equals='Пополнить баланс 💳'))
	dp.register_message_handler(pizza_open_command, Text(equals='Золото 🥇'))
	dp.register_message_handler(pizza_place_command, Text(equals='Посчитать 🥇'))
	dp.register_message_handler(gold_games, Text(equals='Казино $'))
	dp.register_message_handler(up_my_gold, Text(equals='Пополнить 🥇'))
	dp.register_message_handler(get_my_gold, Text(equals='Вывести 🥇'))
	dp.register_message_handler(reviews, Text(equals='Отзывы 👥'))
	dp.register_message_handler(tech_help, Text(equals='Тех.поддержка 👤'))
	dp.register_message_handler(prifile,Text(equals='Профиль 📝'))
	dp.register_message_handler(chests,Text(equals='кейсы 📦'))
	dp.register_message_handler(other_staf,Text(equals='Другие товары 📦'))
	dp.register_message_handler(show_my_turn,Text(equals='Очередь 👤'))
	dp.register_callback_query_handler(balance_uper,lambda x: x.data and x.data.startswith('balance_uper_ '))
	#dp.register_message_handler(balance_uper,state=balance.need_balance)
	dp.register_message_handler(balance_uper_pick,state=balance.need_balance)
	dp.register_message_handler(gold_uper,state=balance_gold.need_balance)
	dp.register_message_handler(gold_geter,state=get_gold.need_get_gold)

	dp.register_message_handler(take_qvest,state=tech_qvest.qvest)
	dp.register_message_handler(count_gold,content_types=['photo'],state=schet_gold.my_gold)

	dp.register_message_handler(add_this_key,state=promo_add.key)

	dp.register_message_handler(count_gold_bet,state=bet_gold.my_bet)
	###########ИНЛАЙН КНОПКИ###########################
	dp.register_callback_query_handler(help_for_1,text='help_1')
	dp.register_callback_query_handler(help_for_2,text='help_2')
	dp.register_callback_query_handler(help_for_3,text='help_3')
	dp.register_callback_query_handler(help_for_4,text='help_4')
	dp.register_callback_query_handler(help_for_5,text='help_5')
	dp.register_callback_query_handler(help_for_6,text='help_6')
	dp.register_callback_query_handler(help_for_7,text='help_7')
	dp.register_callback_query_handler(check,text_contains="cheсk_")
	dp.register_callback_query_handler(need_tech_help,text='help_8_')
	dp.register_callback_query_handler(help_for_back,text='back_get_help')
	dp.register_callback_query_handler(first_staf,text='first_staf_')
	dp.register_callback_query_handler(buy_first_staf,text='buy_first_staf_')
	dp.register_callback_query_handler(back_to_staf,text="back_to_staf_")

	dp.register_callback_query_handler(buy_need_gold,text='buy_need_gold_')

	dp.register_callback_query_handler(another_way_pay,text="another_way_pay_")
	dp.register_callback_query_handler(send_chek_another_way,text="send_chek_another_way_")

	dp.register_callback_query_handler(nachalo,text='nach_chest_')
	dp.register_callback_query_handler(opit_chest,text='opit_chest_')
	dp.register_callback_query_handler(god_chest,text='god_chest_')
	dp.register_callback_query_handler(major_chest,text='major_chest_')
	dp.register_callback_query_handler(gold_chest,text='gold_chest_')
	dp.register_callback_query_handler(free_chest,text='free_chest_')
	dp.register_callback_query_handler(back_to_chest,text='back_to_chest_')

	dp.register_callback_query_handler(buy_nachalo,text='buy_nachalo_')
	dp.register_callback_query_handler(buy_opit_chest,text='buy_opit_chest_')
	dp.register_callback_query_handler(buy_god_chest,text='buy_god_chest_')
	dp.register_callback_query_handler(buy_major_chest,text='buy_major_chest_')
	dp.register_callback_query_handler(buy_gold_chest,text='buy_gold_chest_')
	#dp.register_callback_query_handler(buy_free_chest,text='buy_free_chest')

	dp.register_callback_query_handler(game_tawer,text='game_tawer_')
	dp.register_callback_query_handler(start_game_tawer,text='start_game_tawer_')
	dp.register_message_handler(count_gold_to_tawer,state=gold_to_tawer.gold)
	dp.register_callback_query_handler(tawer_go,text='tawer_go_')
	dp.register_callback_query_handler(tawer_take_my_money,text='tawer_take_my_money_')

	dp.register_callback_query_handler(game_JackPot,text='game_JackPot_')
	dp.register_callback_query_handler(do_gold_bet,text='do_gold_bet_')

	dp.register_callback_query_handler(total_gold_geter,lambda x: x.data and x.data.startswith('Gold_geter_pick '))
	dp.register_callback_query_handler(total_finish_gold_geter,lambda x: x.data and x.data.startswith('Total_gold '))
	dp.register_callback_query_handler(del_support,lambda x: x.data and x.data.startswith('del_support '))	

	dp.register_callback_query_handler(guns_gold_geter,text='guns_gold_geter_')
	dp.register_callback_query_handler(stikers_gold_geter,text='stikers_gold_geter_')
	dp.register_callback_query_handler(trinket_gold_geter,text='trinket_gold_geter_')

	dp.register_callback_query_handler(regular_guns_gold_geter,text='regular_guns_gold_geter_')
	dp.register_callback_query_handler(stattrack_guns_gold_geter,text='stattrack_guns_gold_geter_')
	dp.register_callback_query_handler(arcane_regular_guns_gold_geter,text='arcane_regular_guns_gold_geter_')


	dp.register_callback_query_handler(legendary_regular_guns_gold_geter,text='legendary_regular_guns_gold_geter_')
	dp.register_callback_query_handler(epic_regular_guns_gold_geter,text='epic_regular_guns_gold_geter_')
	dp.register_callback_query_handler(rare_regular_guns_gold_geter,text='rare_regular_guns_gold_geter_')

	dp.register_callback_query_handler(back_ways_gold_get_start,text='back_ways_gold_get_start_')
	dp.register_callback_query_handler(back_guns_gold_geter,text='back_guns_gold_geter_')
	dp.register_callback_query_handler(back_to_regular_guns_gold_geter,text='back_to_regular_guns_gold_geter_')
	dp.register_callback_query_handler(back_to_stattrack_guns_gold_geter,text='back_to_stattrack_guns_gold_geter_')
	dp.register_callback_query_handler(back_to_stikers_gold_geter,text='back_to_stikers_gold_geter_')
	dp.register_callback_query_handler(back_to_trinket_gold_geter,text='back_to_trinket_gold_geter_')

	dp.register_callback_query_handler(cant_found_items,text='arcane_stattrack_guns_gold_geter_')
	dp.register_callback_query_handler(cant_found_items,text='legendary_stattrack_guns_gold_geter_')
	dp.register_callback_query_handler(epic_stattrack_guns_gold_geter,text='epic_stattrack_guns_gold_geter_')
	dp.register_callback_query_handler(rare_stattrack_guns_gold_geter,text='rare_stattrack_guns_gold_geter_')

	dp.register_callback_query_handler(cant_found_items,text='arcane_stikers_gold_geter_')
	dp.register_callback_query_handler(cant_found_items,text='legendary_stikers_gold_geter_')	
	dp.register_callback_query_handler(epic_stikers_gold_geter,text='epic_stikers_gold_geter_')
	dp.register_callback_query_handler(rare_stikers_gold_geter,text='rare_stikers_gold_geter_')

	dp.register_callback_query_handler(cant_found_items,text='arcane_trinket_gold_geter_')
	dp.register_callback_query_handler(cant_found_items,text='legendary_trinket_gold_geter_')	
	dp.register_callback_query_handler(epic_trinket_gold_geter,text='epic_trinket_gold_geter_')
	dp.register_callback_query_handler(rare_trinket_gold_geter,text='rare_trinket_gold_geter_')
	dp.register_callback_query_handler(referr_system,text='referr_system_')

	dp.register_callback_query_handler(top_week,text='top_week_')
	dp.register_callback_query_handler(top_month,text='top_month_')
	dp.register_callback_query_handler(promo_key,text='promo_key_')
	dp.register_message_handler(chek_promo,state=promo.key)

	dp.register_message_handler(send_order_gold,content_types=['photo'],state=photo_gold_geter.photo)
	dp.register_message_handler(send_order_gold,state=photo_gold_geter.photo)
	dp.register_message_handler(take_chek_another_way,content_types=['photo'],state=another_way.chek_way)
	dp.register_message_handler(take_chek_another_way,state=another_way.chek_way)

	dp.register_callback_query_handler(finish_gold_geter,lambda x: x.data and x.data.startswith('finish_gold_geter '))
	dp.register_callback_query_handler(money_back_gold_geter,lambda x: x.data and x.data.startswith('money_back_gold_geter '))
	dp.register_callback_query_handler(give_chek_gold,lambda x: x.data and x.data.startswith('give_chek_gold_ '))
	dp.register_callback_query_handler(otklon_chek_gold,lambda x: x.data and x.data.startswith('otklon_chek_gold_ '))

	dp.register_message_handler(cnt_give_chek_gold,state=give_gold_check.cnt_gold)

##################################ДЛЯ БАНДИТА#################################

	dp.register_callback_query_handler(pick_char_skin_man,text='create_humans_')
	#dp.register_callback_query_handler(skin_ready,lambda x: x.data and x.data.startswith('create_human '))

	dp.register_message_handler(change_can, Text(equals='Поменять работу'))
	dp.register_message_handler(pick_char_skin_gender,state=create_char.skin)
	dp.register_callback_query_handler(pick_hairstyle,lambda x: x.data and x.data.startswith('pick_hirestyle '),state=create_char.hairstyle)
	dp.register_message_handler(pick_name_char,state=create_char.name)

	dp.register_message_handler(jobs,Text(equals='Работа 💸'))
	dp.register_message_handler(scam_info,Text(equals='Похищения 🕸'))
	dp.register_message_handler(show_my_scam_link,Text(equals='Моя ссылка 🔗'))
	dp.register_message_handler(send_vlad,Text(equals='Отправь 🔗'))
	dp.register_message_handler(show_map,Text(equals='Карта 🗺'))
	dp.register_message_handler(pick_new_map,state=set_my_map.new_map)
	dp.register_callback_query_handler(back_to_gold_game,text='back_to_gold_game_')
	dp.register_callback_query_handler(game_JackPot_text,text='game_JackPot_text_')
	
	dp.register_message_handler(donat_menu,Text(equals='Донат 💳'))
	dp.register_message_handler(Moscow_shop,Text(equals='Магазин 🏪'))

	dp.register_message_handler(Barbershop_shop,Text(equals='Парихмахерская 🏪'))

	dp.register_message_handler(pick_mos_shop,state=Mos_shop.shop)
	dp.register_callback_query_handler(scroll_clothes,lambda x: x.data and x.data.startswith('scroll_clothes_ '))
	dp.register_callback_query_handler(exit_clothes_type,lambda x: x.data and x.data.startswith('exit_clothes_type '))
	dp.register_callback_query_handler(buy_clothes,lambda x: x.data and x.data.startswith('buy_clothes '))
	dp.register_callback_query_handler(apply_bay_clothes,lambda x: x.data and x.data.startswith('apply_bay_clothes '))
	dp.register_callback_query_handler(cancel_bay_clothes,lambda x: x.data and x.data.startswith('cancel_bay_clothes'))
	dp.register_message_handler(home_menu,Text(equals='Дом 🏠'))
	dp.register_message_handler(home_buttons,state=home_menu_button.button)

	dp.register_callback_query_handler(bay_wardrobe,lambda x: x.data and x.data.startswith('bay_wardrobe '))
	dp.register_callback_query_handler(apply_bay_wardrobe,lambda x: x.data and x.data.startswith('apply_bay_wardrobe '))	
	dp.register_callback_query_handler(back_main_menu_callback,text='back_main_menu')

	dp.register_message_handler(chenge_wardrobe,state=chenge_wardrobe_state.chenge)

	dp.register_message_handler(bussines,Text(equals='Бизнес 🏢'))
	dp.register_message_handler(bussines_menu,state=bussines_menu_FSM.menu)
	dp.register_message_handler(bussines_storage,state=bussines_menu_FSM.storage)
	dp.register_message_handler(bussines_catalog_way,state=bussines_menu_FSM.catalog)


	dp.register_message_handler(gardener_job,Text(equals='Садовник 🌳'))
	dp.register_message_handler(gardener_job_pick,state=gardener_job_state.point)
