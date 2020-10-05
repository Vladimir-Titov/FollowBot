import os

from aiogram.types import Message, CallbackQuery
from asyncpg.exceptions import UniqueViolationError

from bot import dp, bot
from database import Query
from handlers.parse import ParseShop
from handlers.utils import export_url, pretty_answer
from keyboard.keyboard import keyboard
from price_tracking import PriceTracking


@dp.message_handler(commands=['start', 'help'])
async def start_message(message: Message):
    data = [message.from_user.id, message.from_user.first_name, message.from_user.username]
    try:
        await Query().execute('INSERT INTO users '
                              '(user_id, name, username)'
                              'VALUES($1, $2, $3)', *data)
    except UniqueViolationError:
        pass
    await message.answer(text='Hello')


@dp.message_handler(regexp=r'https?://\w*\d*\.[\w+\S+\d+]+')
async def link(message: Message):
    url = await export_url(message)
    shop_id = await ParseShop().identify_store(url)
    if shop_id == 1:
        try:
            data = await ParseShop(url).parse_ozon()
        except Exception as e:
            print(e)  # todo except
    elif shop_id == 2:
        pass
    try:
        await Query().execute('INSERT INTO product '
                              '(name, link, price, shop_id, user_id) '
                              'VALUES($1, $2, $3, $4, $5)',
                              data['name'], url,
                              data['price'], 1, message.from_user.id)
    except UniqueViolationError:  # todo create my exceptions
        await message.answer(text='Ты уже добавлял такой товар')

    await message.answer(text=f'Название :{data["name"]} \n'
                              f'Цена: {data["price"]}')


@dp.message_handler(commands=['show'])
async def view(message: Message):
    await message.answer(text='Выбери какие товары ты хочешь посмотреть', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ('show_sale', 'show_high', 'all'))
async def show_product(callback_query: CallbackQuery):
    if callback_query.data == 'show_sale':
        result = await Query().execute('SELECT name, price,last_price, link '
                                       'FROM product '
                                       'WHERE user_id = $1 and '
                                       'last_price < price and '
                                       'is_archive = FALSE ', callback_query.from_user.id)

    elif callback_query.data == 'show_high':
        result = await Query().execute('SELECT name, price, last_price, link '
                                       'FROM product '
                                       'WHERE user_id = $1 and '
                                       'last_price > price and '
                                       'is_archive = FALSE ', callback_query.from_user.id)
    else:
        result = await Query().execute('SELECT name, last_price, link '
                                       'FROM product '
                                       'WHERE user_id=$1 and '
                                       'is_archive = FALSE', callback_query.from_user.id)
    answer = await pretty_answer(result)
    if answer == '':
        answer = 'Таких товаров нет'
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=answer, disable_web_page_preview=True)


@dp.message_handler(commands=['update'])
async def update_product(message: Message):
    if message.from_user.id != os.environ['ADMIN_ID']:
        await message.answer(text='Недоступно для тебя')
    else:
        await PriceTracking().run_update()
        await message.answer(text='Цены на товары обновлены')
