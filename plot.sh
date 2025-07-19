#!/bin/bash

# quick_benchmark.sh
# One-liner to run 50 benchmarks and extract execution times

echo "Running 50 benchmarks..."

# Create array to store execution times
exec_times=()

for i in {1..50}; do
    echo -n "Run $i/50: "
    
    # Run function and extract execution time
    exec_time=$(echo "10" | faas-cli invoke goll | grep '{' | jq -r '.executionTime')
    
    if [ "$exec_time" != "null" ] && [ "$exec_time" != "" ]; then
        exec_times+=($exec_time)
        echo "${exec_time} μs"
    else
        echo "Failed"
    fi
    
    sleep 0.5
done

# Save to file
printf '%s\n' "${exec_times[@]}" > execution_times.txt

echo ""
echo "Results saved to execution_times.txt"
echo "Total successful runs: ${#exec_times[@]}"

# Quick stats
if [ ${#exec_times[@]} -gt 0 ]; then
    min=$(printf '%s\n' "${exec_times[@]}" | sort -n | head -1)
    max=$(printf '%s\n' "${exec_times[@]}" | sort -n | tail -1)
    avg=$(printf '%s\n' "${exec_times[@]}" | awk '{sum+=$1} END {print sum/NR}')
    
    echo "Min: $min μs"
    echo "Max: $max μs"
    echo "Avg: $avg μs"
fi

echo ""
echo "To plot results, run:"
echo "python3 -c \"
import matplotlib.pyplot as plt
import numpy as np

# Read data
with open('execution_times.txt', 'r') as f:
    times = [float(line.strip()) for line in f if line.strip()]

# Convert to milliseconds
times_ms = [t/1000 for t in times]

# Create plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Line plot
ax1.plot(range(1, len(times_ms)+1), times_ms, 'b-o', markersize=4)
ax1.set_title('Execution Time vs Run Number')
ax1.set_xlabel('Run Number')
ax1.set_ylabel('Execution Time (ms)')
ax1.grid(True, alpha=0.3)

# Histogram
ax2.hist(times_ms, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
ax2.axvline(np.mean(times_ms), color='red', linestyle='--', label=f'Mean: {np.mean(times_ms):.2f} ms')
ax2.set_title('Execution Time Distribution')
ax2.set_xlabel('Execution Time (ms)')
ax2.set_ylabel('Frequency')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
\""
