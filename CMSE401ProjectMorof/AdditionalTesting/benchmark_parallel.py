import asyncio
import aiohttp
import os
import time
import random
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv('CMC_API_KEY')

# API URL and headers
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

# List of current top 20 crypto symbols
crypto_symbols = [
    'BTC', 'ETH', 'XRP', 'BNB', 'SOL', 'DOGE', 'ADA', 'TRX', 'SUI', 'LINK',
    'AVAX', 'XLM', 'HBAR', 'SHIB', 'LEO', 'TON', 'BCH', 'DOT', 'LTC'
]

# Parallel fetch
async def fetch_price_parallel(session, symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()

        if 'data' in data and symbol in data['data']:
            return symbol, data['data'][symbol]['quote']['USD']['price']
        else:
            print(f"Price for {symbol} not found. Skipping.")
            return symbol, 0.0

async def value_portfolio_parallel(portfolio):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price_parallel(session, symbol) for symbol in portfolio.keys()]
        results = await asyncio.gather(*tasks)

    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = dict(results).get(symbol, 0.0)
        total_value += price * amount
    return total_value

def create_random_portfolio(num_assets, available_symbols):
    symbols = random.sample(available_symbols, num_assets)
    portfolio = {symbol: random.uniform(0.5, 5.0) for symbol in symbols}
    return portfolio

def benchmark_parallel(num_assets_list, available_symbols):
    parallel_times = []

    for num_assets in num_assets_list:
        portfolio = create_random_portfolio(num_assets, available_symbols)
        print(f"\nPortfolio with {num_assets} assets: {portfolio}")

        start_time = time.time()
        total_value = asyncio.run(value_portfolio_parallel(portfolio))
        end_time = time.time()

        elapsed_time = end_time - start_time
        parallel_times.append(elapsed_time)

        print(f"Total Portfolio Value: ${total_value:.2f}")
        print(f"Time Taken (Parallel): {elapsed_time:.2f} seconds")
        print("-" * 50)

    return parallel_times

def plot_results(num_assets_list, parallel_times):
    plt.figure(figsize=(10, 6))
    plt.plot(num_assets_list, parallel_times, label='Parallel', marker='o')
    plt.title('Parallel Portfolio Valuation Timing')
    plt.xlabel('Number of Assets in Portfolio')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('benchmark_parallel_results.png')
    plt.show()

def main():
    available_symbols = crypto_symbols
    num_assets_list = [3, 5, 8, 12]

    print("Starting parallel benchmarking...")
    parallel_times = benchmark_parallel(num_assets_list, available_symbols)
    plot_results(num_assets_list, parallel_times)
    print("Parallel benchmarking completed. Graph saved as 'benchmark_parallel_results.png'.")

if __name__ == '__main__':
    main()

