import requests
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

def fetch_price_serial(symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'data' in data and symbol in data['data']:
        return data['data'][symbol]['quote']['USD']['price']
    else:
        print(f"Price for {symbol} not found. Skipping.")
        return 0.0

def value_portfolio_serial(portfolio):
    total_value = 0.0
    print("\nHoldings breakdown:")
    for symbol, amount in portfolio.items():
        price = fetch_price_serial(symbol)
        holding_value = price * amount
        print(f"{amount:.4f} {symbol} @ ${price:.2f} each = ${holding_value:.2f}")
        total_value += holding_value
    return total_value

def benchmark_serial(portfolios):
    serial_times = []

    for num_assets, portfolio in portfolios.items():
        print(f"\nPortfolio with {num_assets} assets: {portfolio}")

        start_time = time.time()
        total_value = value_portfolio_serial(portfolio)
        end_time = time.time()

        elapsed_time = end_time - start_time
        serial_times.append(elapsed_time)

        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Time Taken (Serial): {elapsed_time:.2f} seconds")
        print("-" * 50)

    return serial_times

def plot_results(num_assets_list, serial_times):
    plt.figure(figsize=(10, 6))
    plt.plot(num_assets_list, serial_times, label='Serial', marker='o')
    plt.title('Serial Portfolio Valuation Timing')
    plt.xlabel('Number of Assets in Portfolio')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('benchmark_serial_results.png')
    plt.show()

def save_results_csv(filename, num_assets_list, times):
    with open(filename, 'w') as f:
        f.write('num_assets,time_seconds\n')
        for num_assets, time_taken in zip(num_assets_list, times):
            f.write(f"{num_assets},{time_taken:.4f}\n")

def main():
    portfolios = load_portfolios_from_txt('portfolios.txt')

    print("Starting serial benchmarking...")
    serial_times = benchmark_serial(portfolios)
    plot_results(list(portfolios.keys()), serial_times)
    save_results_csv('serial_benchmark_results.csv', list(portfolios.keys()), serial_times)
    print("Serial benchmarking completed. Graph saved as 'benchmark_serial_results.png'.")
    print("Serial benchmark timing saved to 'serial_benchmark_results.csv'.")

if __name__ == '__main__':
    main()
