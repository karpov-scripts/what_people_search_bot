from aiogram import Bot, Dispatcher, types

from database import Database
from config import bot_token


bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = Database('database/sqlite3.db')
