from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

#bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token = "5634019011:AAHy7F97ARIn7asdbJHkrUpOxuiA2UpsMRk")


#bot = Bot(token="5395322423:AAHvYJoypGocI5b0GjZUOEy-pOc8LLlVxsU")
dp = Dispatcher(bot, storage=storage)