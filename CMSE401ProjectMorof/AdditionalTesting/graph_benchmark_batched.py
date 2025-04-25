import asyncio
import aiohttp
import requests
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

# List of current top 20 crypto symbols (updated)
crypto_symbols = [
    'BTC', 'ETH', 'XRP', 'BNB', 'SOL', 'DOGE', 'ADA', 'TRX', 'SUI', 'LINK',
    'AVAX', 'XLM', 'HBAR', 'SHIB', 'LEO', 'TON', 'BCH', 'DOT', 'LTC', 'HYPE'
]

# --- Validate symbols with API ---
def validate_symbols(symbol_list):
    valid_symbols = []
    for symbol in symbol_list:
        params = {'symbol': symbol, 'convert': 'USD'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if 'data' in data and symbol in data['data']:
            valid_symbols.append(symbol)
        else:
            print(f"Symbol {symbol} is not valid or not returned by API. Skipping.")
    return valid_symbols

# --- Batch Fetch Serial ---
def fetch_prices_serial(symbols):
    params = {'symbol': ','.join(symbols), 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    prices = {}
    if 'data' in data:
        for symbol in symbols:
            if symbol in data['data']:
                prices[symbol] = data['data'][symbol]['quote']['USD']['price']
            else:
                print(f"Price for {symbol} not found. Skipping.")
                prices[symbol] = 0.0
    else:
        print("API returned no data. Skipping batch.")
        for symbol in symbols:
            prices[symbol] = 0.0

    return prices

def value_portfolio_serial(portfolio):
    symbols = list(portfolio.keys())
    prices = fetch_prices_serial(symbols)

    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = prices.get(symbol, 0.0)
        value = price * amount
        total_value += value
    return total_value

# --- Batch Fetch Parallel ---
async def fetch_prices_parallel(symbols):
    params = {'symbol': ','.join(symbols), 'convert': 'USD'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()

            prices = {}
            if 'data' in data:
                for symbol in symbols:
                    if symbol in data['data']:
                        prices[symbol] = data['data'][symbol]['quote']['USD']['price']
                    else:
                        print(f"Price for {symbol} not found. Skipping.")
                        prices[symbol] = 0.0
            else:
                print("API returned no data. Skipping batch.")
                for symbol in symbols:
                    prices[symbol] = 0.0

            return prices

async def value_portfolio_parallel(portfolio):
    symbols = list(portfolio.keys())
    prices = await fetch_prices_parallel(symbols)

    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = prices.get(symbol, 0.0)
        value = price * amount
        total_value += value
    return total_value

# --- Benchmarking and Plotting ---
def create_random_portfolio(num_assets, available_symbols):
    symbols = random.sample(available_symbols, num_assets)
    portfolio = {symbol: random.uniform(0.5, 5.0) for symbol in symbols}
    return portfolio

def benchmark(num_assets_list, available_symbols):
    serial_times = []
    parallel_times = []

    for num_assets in num_assets_list:
        portfolio = create_random_portfolio(num_assets, available_symbols)

        # Serial timing
        start_serial = time.time()
        value_portfolio_serial(portfolio)
        end_serial = time.time()
        serial_times.append(end_serial - start_serial)

        # Parallel timing
        start_parallel = time.time()
        asyncio.run(value_portfolio_parallel(portfolio))
        end_parallel = time.time()
        parallel_times.append(end_parallel - start_parallel)

        print(f"Completed benchmarking for {num_assets} assets.")

    return serial_times, parallel_times

def plot_results(num_assets_list, serial_times, parallel_times):
    plt.figure(figsize=(10, 6))
    plt.plot(num_assets_list, serial_times, label='Serial', marker='o')
    plt.plot(num_assets_list, parallel_times, label='Parallel', marker='o')
    plt.title('Serial vs Parallel Portfolio Valuation Timing')
    plt.xlabel('Number of Assets in Portfolio')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('benchmark_results.png')
    plt.show()

def main():
    print("Validating available symbols with CoinMarketCap API...")
    available_symbols = validate_symbols(crypto_symbols)

    if not available_symbols:
        print("No valid symbols available. Exiting.")
        return

    num_assets_list = [3, 5, 10, 15, 20]

    print("Starting benchmarking...")
    serial_times, parallel_times = benchmark(num_assets_list, available_symbols)
    plot_results(num_assets_list, serial_times, parallel_times)
    print("Benchmarking completed and graph saved as 'benchmark_results.png'.")

if __name__ == '__main__':
    main()

