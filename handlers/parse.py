import re

import requests
from bs4 import BeautifulSoup


class ParseShop:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 YaBrowser/20.8.3.112 '
                      'Yowser/2.5 Safari/537.36100101 Firefox/36.0'}

    def __init__(self, url: str = None):
        self.url = url

    def get_html(self, **kwargs) -> BeautifulSoup:
        page = requests.get(url=self.url, headers=ParseShop.headers, **kwargs)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    @staticmethod
    async def identify_store(url: str) -> int:
        if 'ozon' in url:
            return 1
        elif 'wildberries' in url:
            return 2

    async def parse_ozon(self, **kwargs):
        html = self.get_html(**kwargs)
        find_name = html.find('h1', class_='b3a8')
        price_sale = html.find('span', class_='b3d b3n5')
        price = html.find('span', class_='b3d')
        regular = re.compile(r'[^\d+]')  # Delete all char that are not numbers
        return {'name': find_name.get_text(),
                'price': regular.sub('', price_sale.get_text())} if price_sale is not None else {
            'name': find_name.get_text(), 'price': regular.sub('', price.get_text())}
