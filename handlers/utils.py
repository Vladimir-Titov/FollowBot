import re

from aiogram.types import Message


async def export_url(message: Message):
    pattern = r'https?://\w*\d*\.[\w+\S+\d+]+'
    url = re.search(pattern, message.text)
    return url.group()


async def pretty_answer(text: str) -> str:
    result = ''
    for word in text:
        if len(word) == 4:
            result += f'Название : {word["name"]} ' \
                      f'\n Цена : {word["last_price"]} , Старая цена : {word["price"]}' \
                      f'\n URL : {word["link"]} \n \n '
        else:
            result += f'Название : {word["name"]} ' \
                  f'\n Цена : {word["last_price"]} ' \
                  f'\n URL : {word["link"]} \n \n '
    return result
