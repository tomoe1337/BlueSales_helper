#from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from vk_maria.types import KeyboardMarkup as ReplyKeyboardMarkup, Button as KeyboardButton, Color
from vk_maria.types.keyboard import OpenLinkButton


kb_client = kb_client_number = kb_client_gold=kb_client_main_menu =kb_for_help=kb_for_contact_or_back=buy_menu=kb_for_staf=kb_chests=main_game_menu=jobs_menu=pick_map_menu = None
'''

b1 = KeyboardButton.Text(Color.PRIMARY,'Золото 🥇')
b2 = KeyboardButton.Text(Color.PRIMARY,'Пополнить баланс 💳')
b3 = KeyboardButton.Text(Color.PRIMARY,'Профиль 📝')
b4 = KeyboardButton.Text(Color.PRIMARY,'кейсы 📦')
b5 = KeyboardButton.Text(Color.PRIMARY,'Отзывы 👥')
b6 = KeyboardButton.Text(Color.PRIMARY,'Другие товары 📦')
b7 = KeyboardButton.Text(Color.PRIMARY,'Тех.поддержка 👤')



popoln = KeyboardButton.Text(Color.PRIMARY,'Пополнить 🥇')
vivod = KeyboardButton.Text(Color.PRIMARY,'Вывести 🥇')
schet = KeyboardButton.Text(Color.PRIMARY,'Посчитать 🥇')
ochered = KeyboardButton.Text(Color.PRIMARY,'Очередь 👤')
g_games = KeyboardButton.Text(Color.PRIMARY,'Игры 🎲')
main_menu = KeyboardButton.Text(Color.PRIMARY,'Главное меню ⬅️')


kb_chests  = kb_for_help = InlineKeyboardMarkup(row_width=2)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_number = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_gold = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_main_menu = ReplyKeyboardMarkup(one_time=True)


kb_client.add_button(b3)

kb_client.add_row()

kb_client.add_button(b4)
kb_client.add_button(b1)
kb_client.add_button(b2)




kb_client.row(b1,b2,b3).row(b4,b5,b6).add(b7)#.row(b1) #.row(b4,b5)
kb_client_gold.row(popoln,vivod).row(schet,ochered).row(g_games,main_menu)
kb_client_main_menu.add(main_menu)
kb_client_number.add(b4)
#kb_client.row(b1,b2,b3)

in1 = InlineKeyboardButton(text='1',callback_data = "help_1")
in2 = InlineKeyboardButton(text='2',callback_data = "help_2")
in3 = InlineKeyboardButton(text='3',callback_data = "help_3")
in4 = InlineKeyboardButton(text='4',callback_data = "help_4")
in5 = InlineKeyboardButton(text='5',callback_data = "help_5")
in6 = InlineKeyboardButton(text='6',callback_data = "help_6")
in7 = InlineKeyboardButton(text='7',callback_data = "help_7")
contack_help = InlineKeyboardButton(text='Связаться',callback_data = "help_8_")
back_help = InlineKeyboardButton(text='Назад',callback_data = "back_get_help")
for_first_staf = InlineKeyboardButton(text='1',callback_data = "first_staf_")

nachalo = InlineKeyboardButton(text='Начало',callback_data = "nach_chest_")
opit_chest = InlineKeyboardButton(text='Опытный',callback_data = "opit_chest_")
god_chest = InlineKeyboardButton(text='Бог',callback_data = "god_chest_")
major_chest = InlineKeyboardButton(text='Мажор',callback_data = "major_chest_")
gold_chest = InlineKeyboardButton(text='Золотой',callback_data = "gold_chest_")
free_chest = InlineKeyboardButton(text='Бесплатный',callback_data = "free_chest_")



kb_chests.add(free_chest).add(nachalo).add(opit_chest).add(god_chest).add(major_chest).add(gold_chest)

kb_for_help = InlineKeyboardMarkup(row_width=2)
kb_for_contact_or_back = InlineKeyboardMarkup(row_width=2)

kb_for_contact_or_back.add(contack_help).add(back_help)
kb_for_help.row(in1,in2,in3).row(in4,in5,in6).add(in7,contack_help)

kb_for_staf=InlineKeyboardMarkup(row_width=2).insert(for_first_staf)

'''

CallbackButton = KeyboardButton.Callback
KeyboardButton = KeyboardButton.Text

kb_chests = ReplyKeyboardMarkup(inline = True)
kb_chests.add_button(CallbackButton(Color.PRIMARY,'Начало',payload = {'data': "nach_chest_"}))
kb_chests.add_row()
#kb_chests.add_button(CallbackButton(Color.PRIMARY,'Опытный',payload = {'data': "opit_chest_"}))
#kb_chests.add_row()
#kb_chests.add_button(CallbackButton(Color.PRIMARY,'Бог',payload = {'data': "god_chest_"}))
#kb_chests.add_row()
#kb_chests.add_button(CallbackButton(Color.PRIMARY,'Мажор',payload = {'data': "major_chest_"}))
#kb_chests.add_row()
#kb_chests.add_button(CallbackButton(Color.PRIMARY,'Золотой',payload = {'data': "gold_chest_"}))
#kb_chests.add_row()
kb_chests.add_button(CallbackButton(Color.PRIMARY,'Бесплатный',payload = {'data': "free_chest_"}))





#trade_first_cb = ReplyKeyboardMarkup(inline = True)

#kb_chests.add_button(CallbackButton(Color.PRIMARY,'Согласиться',payload = {'data': "free_chest_"}))






kb_client_main_menu = ReplyKeyboardMarkup(one_time=False)
kb_client_main_menu.add_button(KeyboardButton(Color.PRIMARY,'Главное меню ⬅️'))

gardener_kb = ReplyKeyboardMarkup()

gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"1"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"2"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"3"))
gardener_kb.add_row()
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"4"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"5"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"6"))
gardener_kb.add_row()

gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"7"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"8"))
gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"9"))
gardener_kb.add_row()

gardener_kb.add_button(KeyboardButton(Color.SECONDARY,"Главное меню ⬅️"))



def main_game_menu(jobs,bussines,home,maps,shops):
	gameMenu = ReplyKeyboardMarkup(one_time = False)
	gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Работа 💸"))
	if shops != 0:
		if maps == "Москва" or shops == 1:
			gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Магазин 🏪"))
		if maps == "Питер":
			gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Парихмахерская 🏪"))
		if maps == "Сочи":
			gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Казино $"))
	if bussines != 0:
		gameMenu.add_row()
		gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Бизнес 🏢"))
	if home != 0:
		gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Дом 🏠"))
	if maps != 0:
		gameMenu.add_button(KeyboardButton(Color.PRIMARY,"Карта 🗺"))
	gameMenu.add_row()
	gameMenu.add_button(KeyboardButton(Color.SECONDARY,"Донат 💳"))
	#gameMenu.add_button(KeyboardButton(Color.SECONDARY,"Тех.поддержка 👤"))
	return gameMenu

def pick_map_menu(maps):
	Mmenu = ReplyKeyboardMarkup()
	if maps != "Москва":
		Mmenu.add_button(KeyboardButton(Color.PRIMARY,"Москва"))
		Mmenu.add_row()
	if maps != "Питер":
		Mmenu.add_button(KeyboardButton(Color.PRIMARY,"Питер"))
		Mmenu.add_row()
	if maps != "Сочи":
		Mmenu.add_button(KeyboardButton(Color.PRIMARY,"Сочи"))
		Mmenu.add_row()
	Mmenu.add_button(KeyboardButton(Color.SECONDARY,"Назад"))
	return Mmenu



def jobs_menu(jobs):
	gameMenu = ReplyKeyboardMarkup()
	gameMenu.add_button(KeyboardButton(Color.PRIMARY, "Похищения 🕸"))
	if jobs > 1:
		gameMenu.add_button(KeyboardButton(Color.PRIMARY,'Садовник 🌳'))
	if jobs > 2:
		gameMenu.add_button(KeyboardButton(Color.PRIMARY,'Работа номер 3'))
	gameMenu.add_row()
	gameMenu.add_button(KeyboardButton(Color.PRIMARY,'Главное меню ⬅️'))
	return gameMenu



def buy_menu(isUrl=True, url='',bill=''):
	qiwiMenu = ReplyKeyboardMarkup(inline = True)
	if isUrl:
		#btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату", url=url)
		qiwiMenu.add_button(OpenLinkButton(link = url ,label = "Ссылка на оплату"))

	#btnCheckQIWI = InlineKeyboardButton(text="Проверить оплату", callback_data="cheсk_"+bill)	
	qiwiMenu.add_button(CallbackButton(Color.PRIMARY,"Проверить оплату", payload = {'data':"cheсk_"+bill}))

	return qiwiMenu





