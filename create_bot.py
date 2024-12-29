from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

storage=MemoryStorage()

bot = Bot(token = BOT_TOKEN)

dp = Dispatcher(bot, storage=storage)