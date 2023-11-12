from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()
