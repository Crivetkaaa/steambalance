import aiohttp
from bs4 import BeautifulSoup as bs
import json
import asyncio


class BalanceChecker:
    @classmethod
    async def get_balance(cls, login):
        url = 'https://steamcommunity.com/login/home/?goto='
        cookies = await cls.create_cookies(login)
        async with aiohttp.ClientSession(cookies=cookies) as sessoin:
            async with sessoin.get(url) as response:
                response_html = await response.text()
                soup = bs(response_html, 'lxml')
                balance = soup.find('a', class_='global_action_link').text
                return balance

    @staticmethod
    async def create_cookies(login) -> dict:
        return_cookies = {}
        with open(f'cookies/cookies-{login}', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            return_cookies[cookie['name']] = cookie['value']
        return return_cookies
