import matplotlib.pyplot as plt
import pandas as pd

# Load the benchmark data
serial_df = pd.read_csv('serial_benchmark_results.csv')
parallel_df = pd.read_csv('parallel_benchmark_results.csv')

# Extract data
num_assets_serial = serial_df['num_assets']
times_serial = serial_df['time_seconds']

num_assets_parallel = parallel_df['num_assets']
times_parallel = parallel_df['time_seconds']

# --- Plot 1: Serial vs Parallel Timing ---
plt.figure(figsize=(10, 6))
plt.plot(num_assets_serial, times_serial, label='Serial', marker='o')
plt.plot(num_assets_parallel, times_parallel, label='Parallel', marker='o')
plt.title('Serial vs Parallel Portfolio Valuation Timing')
plt.xlabel('Number of Assets in Portfolio')
plt.ylabel('Time Taken (seconds)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('serial_vs_parallel_timing.png')
plt.show()

# --- Plot 2: Speedup Factor (Serial Time / Parallel Time) ---
speedup = times_serial / times_parallel

plt.figure(figsize=(10, 6))
plt.plot(num_assets_serial, speedup, label='Speedup (Serial / Parallel)', marker='o', color='green')
plt.title('Speedup Achieved by Parallelization')
plt.xlabel('Number of Assets in Portfolio')
plt.ylabel('Speedup Factor')
plt.axhline(y=1, color='red', linestyle='--', label='No Speedup')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('speedup_factor.png')
plt.show()
