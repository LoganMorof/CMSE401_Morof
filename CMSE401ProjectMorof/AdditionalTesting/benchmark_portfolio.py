import asyncio
import aiohttp
import requests
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

# --- Serial Version Functions ---
def fetch_price_serial(symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    price = data['data'][symbol]['quote']['USD']['price']
    return price

def value_portfolio_serial(portfolio):
    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = fetch_price_serial(symbol)
        value = price * amount
        total_value += value
    return total_value

# --- Parallel Version Functions ---
async def fetch_price_parallel(session, symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()
        price = data['data'][symbol]['quote']['USD']['price']
        return symbol, price

async def fetch_all_prices_parallel(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price_parallel(session, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        return dict(results)

async def value_portfolio_parallel(portfolio):
    prices = await fetch_all_prices_parallel(portfolio.keys())
    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = prices[symbol]
        value = price * amount
        total_value += value
    return total_value

# --- Benchmark Runner ---
def run_benchmark():
    portfolio = read_portfolio('portfolio.txt')

    # Serial Timing
    print("Running Serial Version...")
    start_serial = time.time()
    total_serial = value_portfolio_serial(portfolio)
    end_serial = time.time()
    time_serial = end_serial - start_serial

    # Parallel Timing
    print("Running Parallel Version...")
    start_parallel = time.time()
    total_parallel = asyncio.run(value_portfolio_parallel(portfolio))
    end_parallel = time.time()
    time_parallel = end_parallel - start_parallel

    # Results
    print("\n--- Benchmark Results ---")
    print(f"Total Portfolio Value (Serial):  ${total_serial:.2f}")
    print(f"Total Portfolio Value (Parallel): ${total_parallel:.2f}")
    print(f"Time Taken (Serial):   {time_serial:.2f} seconds")
    print(f"Time Taken (Parallel): {time_parallel:.2f} seconds")

    speedup = time_serial / time_parallel if time_parallel > 0 else float('inf')
    print(f"Speedup (Serial / Parallel): {speedup:.2f}x faster")

if __name__ == '__main__':
    run_benchmark()

