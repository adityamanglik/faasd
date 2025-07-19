#!/usr/bin/env python3
"""
plot_results.py
Script to visualize execution times from the benchmark results
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import pandas as pd

def load_results(filename='results.json'):
    """Load results from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please run the benchmark script first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return None

def plot_execution_times(results):
    """Create comprehensive plots of execution times"""
    
    # Extract data
    runs = [r['run'] for r in results]
    exec_times = [r['executionTime'] for r in results]  # in microseconds
    heap_alloc = [r['heapAlloc'] for r in results]
    num_gc = [r['NumGC'] for r in results]
    
    # Convert to milliseconds for better readability
    exec_times_ms = [t / 1000 for t in exec_times]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('FaaS Function Performance Analysis (100 Runs)', fontsize=16, fontweight='bold')
    
    # 1. Execution Time Over Runs
    axes[0, 0].plot(runs, exec_times_ms, 'b-o', linewidth=2, markersize=4, alpha=0.7)
    axes[0, 0].set_title('Execution Time vs Run Number', fontweight='bold')
    axes[0, 0].set_xlabel('Run Number')
    axes[0, 0].set_ylabel('Execution Time (ms)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(runs, exec_times_ms, 1)
    p = np.poly1d(z)
    axes[0, 0].plot(runs, p(runs), "r--", alpha=0.8, label=f'Trend: {z[0]:.3f}x + {z[1]:.3f}')
    axes[0, 0].legend()
    
    # 2. Execution Time Distribution
    axes[0, 1].hist(exec_times_ms, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 1].axvline(np.mean(exec_times_ms), color='red', linestyle='--', 
                      label=f'Mean: {np.mean(exec_times_ms):.2f} ms')
    axes[0, 1].axvline(np.median(exec_times_ms), color='green', linestyle='--', 
                      label=f'Median: {np.median(exec_times_ms):.2f} ms')
    axes[0, 1].set_title('Execution Time Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Execution Time (ms)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Memory Usage vs Execution Time
    axes[1, 0].scatter(exec_times_ms, [h/1024/1024 for h in heap_alloc], 
                      alpha=0.6, s=50, c='purple')
    axes[1, 0].set_title('Memory vs Execution Time', fontweight='bold')
    axes[1, 0].set_xlabel('Execution Time (ms)')
    axes[1, 0].set_ylabel('Heap Allocated (MB)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Garbage Collection vs Execution Time
    axes[1, 1].scatter(exec_times_ms, num_gc, alpha=0.6, s=50, c='orange')
    axes[1, 1].set_title('GC Count vs Execution Time', fontweight='bold')
    axes[1, 1].set_xlabel('Execution Time (ms)')
    axes[1, 1].set_ylabel('Number of GC Runs')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"execution_analysis_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as: {filename}")
    
    plt.show()

def print_statistics(results):
    """Print detailed statistics"""
    exec_times = [r['executionTime'] for r in results]
    exec_times_ms = [t / 1000 for t in exec_times]
    heap_alloc = [r['heapAlloc'] for r in results]
    num_gc = [r['NumGC'] for r in results]
    
    print("\n" + "="*50)
    print("DETAILED STATISTICS")
    print("="*50)
    
    print(f"Total runs: {len(results)}")
    print(f"Container ID: {results[0]['containerId']}")
    print(f"Array size: {results[0]['arraysize']}")
    print(f"GOGC setting: {results[0]['GOGC']}")
    print(f"Memory limit: {results[0]['GOMEMLIMIT']}")
    
    print("\nExecution Time Statistics (microseconds):")
    print(f"  Mean: {np.mean(exec_times):.2f} μs ({np.mean(exec_times_ms):.2f} ms)")
    print(f"  Median: {np.median(exec_times):.2f} μs ({np.median(exec_times_ms):.2f} ms)")
    print(f"  Min: {min(exec_times)} μs ({min(exec_times_ms):.2f} ms)")
    print(f"  Max: {max(exec_times)} μs ({max(exec_times_ms):.2f} ms)")
    print(f"  Std Dev: {np.std(exec_times):.2f} μs ({np.std(exec_times_ms):.2f} ms)")
    print(f"  Coefficient of Variation: {(np.std(exec_times)/np.mean(exec_times))*100:.2f}%")
    
    print("\nMemory Statistics:")
    print(f"  Mean Heap Alloc: {np.mean(heap_alloc)/1024/1024:.2f} MB")
    print(f"  Min Heap Alloc: {min(heap_alloc)/1024/1024:.2f} MB")
    print(f"  Max Heap Alloc: {max(heap_alloc)/1024/1024:.2f} MB")
    
    print("\nGarbage Collection Statistics:")
    print(f"  Mean GC Count: {np.mean(num_gc):.2f}")
    print(f"  Min GC Count: {min(num_gc)}")
    print(f"  Max GC Count: {max(num_gc)}")
    
    # Performance patterns
    print("\nPerformance Patterns:")
    first_10_avg = np.mean(exec_times[:10])
    last_10_avg = np.mean(exec_times[-10:])
    print(f"  First 10 runs average: {first_10_avg:.2f} μs")
    print(f"  Last 10 runs average: {last_10_avg:.2f} μs")
    print(f"  Difference: {last_10_avg - first_10_avg:.2f} μs")
    
    if last_10_avg > first_10_avg:
        print("  → Performance degradation detected")
    elif last_10_avg < first_10_avg:
        print("  → Performance improvement detected")
    else:
        print("  → Stable performance")

def main():
    """Main function"""
    print("Loading benchmark results...")
    results = load_results()
    
    if results is None:
        return
    
    if len(results) == 0:
        print("No results found in the file.")
        return
    
    print(f"Loaded {len(results)} benchmark results")
    
    # Print statistics
    print_statistics(results)
    
    # Create plots
    print("\nGenerating plots...")
    plot_execution_times(results)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
