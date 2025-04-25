import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('CMC_API_KEY')
headers = {'X-CMC_PRO_API_KEY': API_KEY}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

async def fetch_price(symbol):
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'symbol': symbol, 'convert': 'USD'}
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            price = data['data'][symbol]['quote']['USD']['price']
            print(f'{symbol}: ${price:.2f}')

asyncio.run(fetch_price('BTC'))

