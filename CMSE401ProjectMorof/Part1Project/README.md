# Software Abstract
This software example demonstrates the use of Python for real-time cryptocurrency price tracking utilizing asynchronous programming (asyncio) in combination with asynchronous HTTP requests (aiohttp). Specifically, this example leverages the CoinMarketCap API to fetch cryptocurrency prices concurrently, reducing the total retrieval time compared to sequential fetching methods.

## What is this Software?
The Crypto Portfolio Price Tracker is an example of application-level software leveraging modern asynchronous programming techniques. It integrates Python's built-in concurrency framework (asyncio) with the efficient asynchronous HTTP client library (aiohttp) to create a robust and high-performance API request handler.

The primary functions of this software include:

- Fetching real-time cryptocurrency prices concurrently.
- Displaying retrieved price data clearly and succinctly in a command-line environment.
- Demonstrating how asynchronous methods can significantly improve efficiency when interacting with web-based APIs.

## Applications in Science and Engineering
This type of software is highly relevant across multiple fields in science, engineering, and especially finance and data science, due to its capability to handle extensive real-time data efficiently.

Specific Applications Include:

Financial Analysis & Trading Systems:
- Utilized in algorithmic trading to rapidly process and analyze financial data for arbitrage detection and real-time price monitoring.

Data Engineering and Science:
- Essential for efficiently fetching and aggregating large datasets, particularly from web-based sources, for immediate analytical processing and machine learning applications.

Real-Time Systems and Dashboards:
- Commonly used for creating real-time visualization dashboards, alert systems, or decision-support tools in scientific research, IoT monitoring, and engineering analytics.

## Software Type
This software can be categorized as an application-level programming tool, which serves as an efficient wrapper around external API services. It simplifies the complex task of concurrent network operations, abstracting away intricate management of parallel HTTP requests through simple and maintainable Python code.

Software Layers & Roles:

- API Layer (CoinMarketCap API): Provides comprehensive real-time cryptocurrency market data.
- Middleware Layer (aiohttp): Handles asynchronous network communication and HTTP management.
- Programming Framework (asyncio): Coordinates and schedules concurrent tasks for optimized performance.
- Application Layer (Python Script): Provides an intuitive interface for users to fetch and interact with real-time crypto prices effectively.

# Installation Instructions
This project requires a few Python packages that may not be readily available on the HPCC, so it is recommended to run the example code locally for ease of setup, especially when working with aiohttp.

## 1. Create a CoinMarketCap Account for a Free API Key
Go to https://coinmarketcap.com/api/ and follow their account setup instructions to receive your free API key.

## 2. Load Python
If running on the HPCC (package is not available on the HPCC unfortunetly so these tests are done locally):
```
module load Python/3.11.0
```

If running locally, make sure you are using Python 3.8 or higher.

## 3. Install Required Python Packages
Use your preferred package manager. For example:
```
mamba install aiohttp python-dotenv
```
Or, if using pip:
```
pip install aiohttp python-dotenv
```

## 4. Create a .env File to Store Your API Key
Create a file named `.env` in the same directory as your script:
```
vim .env
```

Inside the file, add the following line:
```
CMC_API_KEY=your_actual_coinmarketcap_api_key
```

Replace `your_actual_coinmarketcap_api_key` with the API key you received. Save and close the file.

## 5. Run the Example Script
Execute the script using:
```
python fetch_prices.py
```

Expected output:
```
BTC: $94869.05
```
# Optional: Example SLURM Submission Script (For HPCC Use)

> **Note:** The following example submission script demonstrates how you would run this project on the HPCC if the required packages (`aiohttp`, `python-dotenv`) were available via system modules or could be pre-installed in a virtual environment. However, due to compatibility and availability issues, this setup may not function as intended on the HPCC. This script is included for instructional purposes only.

## Example `submit_job.sb`:

```bash
#!/bin/bash
#SBATCH --job-name=fetch_crypto_prices
#SBATCH --output=crypto_output.out
#SBATCH --error=crypto_error.err
#SBATCH --time=00:05:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1

# Load Python module
module load Python

# Activate virtual environment if dependencies are pre-installed
# source crypto-env/bin/activate

# Run the Python script
python fetch_prices.py
```

## How to Use (if applicable)
If this were supported on the HPCC, you would submit the job using:
```
sbatch submit_job.sb
```

You could then monitor the job with:
```
squeue -u <your_net_id>
```

And review the output once completed in:
- `crypto_output.out` for standard output
- `crypto_error.err` for errors
