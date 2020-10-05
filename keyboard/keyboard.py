from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

sale_button = InlineKeyboardButton(text='Цена снизилась', callback_data='show_sale')
high_button = InlineKeyboardButton(text='Цена выше', callback_data='show_high')
all_button = InlineKeyboardButton(text='Все товары', callback_data='all')
keyboard = InlineKeyboardMarkup().add(all_button, sale_button, high_button)
