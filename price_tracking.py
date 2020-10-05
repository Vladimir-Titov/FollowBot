from datetime import datetime

from database.database import Query
from handlers.parse import ParseShop


class PriceTracking:
    now_time = datetime.now()

    @staticmethod
    async def get_url_and_price():
        data = await Query().execute('SELECT link, price '
                                     'FROM product WHERE shop_id = 1')
        return data

    async def update_ozon_price(self):
        for data in await self.get_url_and_price():
            try:
                payload = await ParseShop(url=data['link']).parse_ozon()
                await Query().execute('UPDATE product SET last_price=$1 '
                                      ', last_update_date = $2 WHERE link=$3',
                                      payload["price"], self.now_time,
                                      data["link"])
            except AttributeError:
                continue

    async def run_update(self):
        await self.update_ozon_price()
