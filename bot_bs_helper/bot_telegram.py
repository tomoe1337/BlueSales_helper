from aiogram.utils import executor
from create_bot import dp
from handlers import Blue_Sales
from handlers import others

async def on_start(_):
	print('Polling started successfully!')

Blue_Sales.register_handlers_client(dp)
others.register_handlers_others(dp)

executor.start_polling(dp,skip_updates=True, on_startup=on_start)
