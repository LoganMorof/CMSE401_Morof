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

# Fetch price (serially, one at a time)
def fetch_price(symbol):
    params = {'symbol': symbol, 'convert': 'USD'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    price = data['data'][symbol]['quote']['USD']['price']
    return price

# Main valuation function
def value_portfolio(portfolio):
    total_value = 0.0
    for symbol, amount in portfolio.items():
        price = fetch_price(symbol)
        value = price * amount
        print(f"{symbol}: {amount} × ${price:.2f} = ${value:.2f}")
        total_value += value
    return total_value

# Timing wrapper
def main():
    portfolio = read_portfolio('basic_portfolio.txt')
    start_time = time.time()
    total_value = value_portfolio(portfolio)
    end_time = time.time()
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")
    print(f"Time Taken (serial version): {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()

