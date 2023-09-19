from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

#bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token = "5434620672:AAEuKlg3l0Iczybb3rAdnIugIERwnRbZAIM")

#bot = Bot(token="5395322423:AAHvYJoypGocI5b0GjZUOEy-pOc8LLlVxsU")
dp = Dispatcher(bot, storage=storage)