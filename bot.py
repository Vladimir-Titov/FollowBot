import logging
import os
from aiogram import Dispatcher, Bot

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ['TOKEN']


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
