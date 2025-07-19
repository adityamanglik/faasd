#!/bin/zsh
# Number of requests to send
TOTAL_REQUESTS=100

# Load balancer URL
URL="http://localhost:5000"

echo "Sending $TOTAL_REQUESTS requests to $URL..."

for ((i = 1; i <= TOTAL_REQUESTS; i++)); do
  # Random value of n between 5 and 15
  n=$((RANDOM % 11 + 5))

  # Send POST request
  response=$(curl -s -X POST "$URL" -d "$n")

  # Show which function responded
  echo "[$i] Fibonacci($n) → $response"
done