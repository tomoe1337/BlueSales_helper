from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db


async def on_start(_):
	print('Работаем')
	sqlite_db.sql_start()


from handlers import Blue_Sales


Blue_Sales.register_handlers_client(dp)
#admin.register_handlers_admin(dp)
#others.register_handlers_others(dp)

executor.start_polling(dp,skip_updates=True, on_startup=on_start)
