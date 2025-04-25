import asyncio
import aiohttp
import os
import time
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

def load_portfolios_from_txt(filename):
    portfolios = {}
    current_portfolio = {}
    current_size = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                if current_portfolio and current_size:
                    portfolios[current_size] = current_portfolio
                    current_portfolio = {}
                current_size = int(line.split()[3])
            else:
                symbol, amount = line.split()
                current_portfolio[symbol.upper()] = float(amount)

        if current_portfolio and current_size:
            portfolios[current_size] = current_portfolio

    return portfolios

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
    prices = dict(results)

    print("\nHoldings breakdown:")
    for symbol, amount in portfolio.items():
        price = prices.get(symbol, 0.0)
        holding_value = price * amount
        print(f"{amount:.4f} {symbol} @ ${price:.2f} each = ${holding_value:.2f}")
        total_value += holding_value
    return total_value

def benchmark_parallel(portfolios):
    parallel_times = []

    for num_assets, portfolio in portfolios.items():
        print(f"\nPortfolio with {num_assets} assets: {portfolio}")

        start_time = time.time()
        total_value = asyncio.run(value_portfolio_parallel(portfolio))
        end_time = time.time()

        elapsed_time = end_time - start_time
        parallel_times.append(elapsed_time)

        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
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

def save_results_csv(filename, num_assets_list, times):
    with open(filename, 'w') as f:
        f.write('num_assets,time_seconds\n')
        for num_assets, time_taken in zip(num_assets_list, times):
            f.write(f"{num_assets},{time_taken:.4f}\n")

def main():
    portfolios = load_portfolios_from_txt('portfolios.txt')

    print("Starting parallel benchmarking...")
    parallel_times = benchmark_parallel(portfolios)
    plot_results(list(portfolios.keys()), parallel_times)
    save_results_csv('parallel_benchmark_results.csv', list(portfolios.keys()), parallel_times)
    print("Parallel benchmarking completed. Graph saved as 'benchmark_parallel_results.png'.")
    print("Parallel benchmark timing saved to 'parallel_benchmark_results.csv'.")

if __name__ == '__main__':
    main()
