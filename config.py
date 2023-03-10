import asyncio
import logging

from aiogram.utils.exceptions import Unauthorized
from pyqiwip2p import QiwiP2P
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database

BOT_TOKEN = '6181317526:AAFPFEQbIYS9SOv-UCOSG2NA1SB5JmPQoVI'

bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database("bot_database.db")

# server = Flask(__name__)
# logger = aiogram.dispatcher.middlewares.log
# logger.setLevel(logging.DEBUG)

GROUPS = {
    "🔥Поставщики(1999₽)🔥": ("-1001388598795", 1999),
    "🔥Поставщики Товарка(999₽)🔥": ("-1001088486978", 999),
    "🔥Товарка(749₽)🔥": ("-1001579041927", 749),
    "🔥Товарочка(499₽)🔥": ("-1001169373505", 499),
    "🔥Grand-Opt(499₽)🔥": ("-1001579396634", 499),
    "🔥Поставки Оптом(449₽)🔥": ("-1001297013878", 499),
    "🔥Товарочка(399₽)🔥": ("-1001439847153", 399),
    "🔥Товарный бизнес(199₽)🔥": ("-1001612357609", 199)
}

APP_URL = 'https://academyhelperbot.herokuapp.com/' + BOT_TOKEN

UKASSA_TOKEN = "390540012:LIVE:27750"
SBER_TOKEN = '401643678:TEST:df285492-0a8c-4c66-9b63-2fa28cb6ec59'

p2p = QiwiP2P(auth_key='eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InNzczVvMC0wMCIsInVzZXJfaWQ'
                       'iOiI3OTg5NzUwNTg2MCIsInNlY3JldCI6ImI2MmE1MWYzYmViOTliZmJjYTAwM2U1YjFiNmM4MmQ1MTQ0Mzg5MGJhZWVlMj'
                       'AxMmZlZTdhYmExZDFiM2IyMjUifX0=')
