from vk_maria import Vk as Bot
from vk_maria.dispatcher import Dispatcher
import os
from vk_maria.dispatcher.fsm.storage.memory import MemoryStorage
from vk_maria.upload import Upload

storage=MemoryStorage()

#bot = Bot(token=os.getenv('TOKEN'))
#zero
#bot = Bot(access_token="vk1.a.v-Py36GfgUEp4fpLZVxttMnNbk21Iy7vB8L0lj0k87bhV-IEo08-6OxE1UYB1IVSW0I9uS-tRajPq-q9th055-Up2VeGQzA3G106dtLzR130Vs6rnu2t5P_HLZIkS_j_mJxcMPL_NNgngY6QAQ3X9Cafbnjl7tfWsv0wlakUaOpcF22qBY2uA2hlaE9jUxV8zPS4zcaNE0bLEsak0ObFTA")
#bot = Bot(access_token="vk1.a.HDFP8iCyPsNYM0piCzWLuOdLEHV8hPhRqA3G0HGPwW-WE2R7b-BVbF5n6LEWMf4GmiaT3xxzraAW1TcO8rONiYRdnU42oXshsUsb-ZkM-Sxeyn-AMz2pLuFwBjCiVQ3TtfYbzHWEauwYWmhNaUjkpMi-MiAZkN9ZgFherppZrWseF--WcIuMJZ2czOUmUrPv6-NDXoWNGsc5Y_4yWx2a7A")
bot = Bot(token = "5634019011:AAHy7F97ARIn7asdbJHkrUpOxuiA2UpsMRk")

upload = Upload(bot)
dp = Dispatcher(bot, storage=storage)