import aiohttp
import asyncio
import os
import time
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv('CMC_API_KEY')

# API URL and headers
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

# Read portfolio
def read_portfolio(filename):
    portfolio = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                symbol, amount = parts
                portfolio[symbol.upper()] = float(amount)
    return portfolio

# Async function to fetch a single price
async def fetch_price(session, symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()
        price = data['data'][symbol]['quote']['USD']['price']
        return symbol, price

# Async function to fetch all prices
async def fetch_all_prices(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        return dict(results)

# Main valuation function
async def value_portfolio(portfolio):
    prices = await fetch_all_prices(portfolio.keys())
    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = prices[symbol]
        value = price * amount
        print(f"{symbol}: {amount} × ${price:.2f} = ${value:.2f}")
        total_value += value
    return total_value

# Timing wrapper
def main():
    portfolio = read_portfolio('basic_portfolio.txt')
    start_time = time.time()
    total_value = asyncio.run(value_portfolio(portfolio))
    end_time = time.time()
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    print(f"Time Taken (parallel version): {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()

