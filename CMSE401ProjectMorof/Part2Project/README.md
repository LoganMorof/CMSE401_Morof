# Crypto Portfolio Valuation Project

This project demonstrates how to value a cryptocurrency portfolio using live price data from the CoinMarketCap (CMC) API.  
It also compares the performance of serial vs parallel API calls when valuing a portfolio of different sizes.

---

## 📥 Setup Instructions

1. **Clone or download the project folder** to your local machine.

2. **Install required Python packages** if you haven't already:
   ```bash
   pip install aiohttp python-dotenv matplotlib pandas
   ```

3. **Get a free CoinMarketCap API Key**:
   - Visit [https://coinmarketcap.com/api/](https://coinmarketcap.com/api/).
   - Create a free account.
   - Copy your personal API key.

4. **Create a `.env` file** in your project directory:
   ```
   CMC_API_KEY=your_actual_api_key_here
   ```

   This key is needed for all scripts to access live cryptocurrency data.

---

## 📁 Project File Overview

### Basic Portfolio Test

These files perform a **simple portfolio valuation** using either serial or parallel fetching:

- `basic_portfolio.txt`  
  A small manually defined portfolio (fixed assets and amounts).

- `portfolio_serial.py`  
  - Reads the `basic_portfolio.txt` file.
  - Fetches live crypto prices **serially** (one by one).
  - Prints the individual holding values and total portfolio value.

- `portfolio_parallel.py`  
  - Reads the same `basic_portfolio.txt` file.
  - Fetches live crypto prices **in parallel** (asynchronous multiple calls).
  - Prints the individual holding values and total portfolio value.

Use these scripts for a quick demo of serial vs parallel behavior on a simple, small portfolio.

---

### Benchmarking Portfolio Tests

This is the **full benchmarking and performance comparison** part of the project.

- `portfolios.txt`  
  - Predefined larger portfolios (3, 5, 8, and 12 assets) used for timing tests.
  - No randomness — fully reproducible across runs.

- `benchmark_serial.py`  
  - Values portfolios **serially**.
  - Records the time taken for each portfolio.
  - Plots timing results.
  - Saves detailed timing data into `serial_benchmark_results.csv`.

- `benchmark_parallel.py`  
  - Values portfolios **in parallel** using `asyncio` and `aiohttp`.
  - Records the time taken for each portfolio.
  - Plots timing results.
  - Saves detailed timing data into `parallel_benchmark_results.csv`.

- `compare_serial_parallel.py`  
  - Reads the timing results from the two CSV files.
  - Creates two comparison plots:
    - **Serial vs Parallel Timing** (`serial_vs_parallel_timing.png`)
    - **Speedup Factor** (`speedup_factor.png`)
  - Highlights the differences between serial and parallel performance.

---

## 📈 Output Files

After running the scripts, you will generate:

- `benchmark_serial_results.png` – Timing graph for serial valuation.
- `benchmark_parallel_results.png` – Timing graph for parallel valuation.
- `serial_benchmark_results.csv` – Raw timing results for serial runs.
- `parallel_benchmark_results.csv` – Raw timing results for parallel runs.
- `serial_vs_parallel_timing.png` – Side-by-side timing comparison plot.
- `speedup_factor.png` – Speedup factor plot showing how much faster parallel execution is.

---

## 🛠 How to Run Everything

1. Set up your `.env` file with your API key.
2. (Optional) Start with `portfolio_serial.py` and `portfolio_parallel.py` for a quick simple test.
3. Run the full benchmark tests:
   ```bash
   python benchmark_serial.py
   python benchmark_parallel.py
   ```
4. Compare results:
   ```bash
   python compare_serial_parallel.py
   ```

---

## 📋 Notes and Important Information

- **API Rate Limits:** The CoinMarketCap Free API limits you to 30 requests per minute.  
  This project stays within that limit safely by controlling portfolio sizes and splitting benchmarks into two scripts.

- **Expected Behavior:**  
  Parallel execution reduces wait time when the server allows concurrent responses.  
  However, public APIs like CoinMarketCap may introduce server-side bottlenecks that affect overall speedup potential.

- **Portfolio Values:**  
  Portfolio valuations are based on **live prices** at the time of execution.  
  Results may vary slightly if re-run at a different time.
