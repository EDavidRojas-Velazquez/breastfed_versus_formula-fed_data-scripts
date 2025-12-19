#!/bin/bash

# Define paths
DB="/home/david/kraken_db"
INPUT_DIR="/home/david/kraken_experiments/kraken_rep"
OUTPUT_DIR="/home/david/kraken_experiments/bracken_res"

# Parameters
READ_LEN=100
LEVEL="S"

# Loop through all .report files in INPUT_DIR
for file in "$INPUT_DIR"/*.report; do
    # Extract the base name without extension
    base=$(basename "$file" .report)

    # Define output path
    output="$OUTPUT_DIR/${base}_${LEVEL}.bracken"

    # Run bracken
    echo "Processing $file..."
    bracken -d "$DB" -i "$file" -o "$output" -r "$READ_LEN" -l "$LEVEL"
done

echo "All Bracken analyses completed!"

