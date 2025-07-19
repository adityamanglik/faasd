#!/bin/bash

# benchmark_runner.sh
# Script to run the faasd function 100 times and collect execution times

OUTPUT_FILE="execution_times.json"
TEMP_FILE="temp_output.json"
RESULTS_FILE="results.json"

echo "Starting benchmark run..."
echo "Running function 300 times..."

# Initialize results array
echo "[]" > "$RESULTS_FILE"

for i in {1..300}; do
    echo "Run $i/100"
    
    # Run the function and capture output
    echo "10" | curl -X POST -d @- http://localhost:5000 | grep '{' | jq '.' > "$TEMP_FILE"
    
    # Check if the command was successful
    if [ $? -eq 0 ]; then
        # Add run number to the JSON
        jq ". + {\"run\": $i}" "$TEMP_FILE" > "${TEMP_FILE}.tmp" && mv "${TEMP_FILE}.tmp" "$TEMP_FILE"
        
        # Append to results array
        jq ". + [$(cat $TEMP_FILE)]" "$RESULTS_FILE" > "${RESULTS_FILE}.tmp" && mv "${RESULTS_FILE}.tmp" "$RESULTS_FILE"
        
        # Extract execution time for quick preview
        exec_time=$(jq '.executionTime' "$TEMP_FILE")
        echo "  Execution time: $exec_time microseconds"
    else
        echo "  Error: Function call failed"
    fi
done

# Clean up temporary file
rm -f "$TEMP_FILE" "${TEMP_FILE}.tmp" "${RESULTS_FILE}.tmp"

echo "Benchmark complete!"
echo "Results saved to: $RESULTS_FILE"
echo ""
echo "Quick stats:"
echo "============"

# Extract execution times and calculate basic stats
jq -r '.[] | .executionTime' "$RESULTS_FILE" | sort -n > exec_times.txt

if [ -s exec_times.txt ]; then
    min_time=$(head -1 exec_times.txt)
    max_time=$(tail -1 exec_times.txt)
    avg_time=$(awk '{sum+=$1} END {print sum/NR}' exec_times.txt)
    median_time=$(awk '{a[NR]=$1} END {print (NR%2==1)?a[(NR+1)/2]:(a[NR/2]+a[NR/2+1])/2}' exec_times.txt)
    
    echo "Min execution time: $min_time μs"
    echo "Max execution time: $max_time μs"
    echo "Average execution time: $avg_time μs"
    echo "Median execution time: $median_time μs"
    
    # Clean up
    rm exec_times.txt
fi

echo ""
echo "Run the Python plotting script to visualize the results:"
echo "python3 plot_results.py"
