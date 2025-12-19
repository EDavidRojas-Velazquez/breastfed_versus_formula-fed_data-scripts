#!/bin/bash

# Define paths
DB="/home/david/kraken_db"
INPUT_DIR="/home/david/kraken_experiments/filtered"
OUTPUT_DIR="/home/david/kraken_experiments/kraken_rep"

# Number of threads
THREADS=20

# Loop through all .fastq.gz files in INPUT_DIR
for file in "$INPUT_DIR"/*.fastq.gz; do
    # Extract the base name without extension
    base=$(basename "$file" .fastq.gz)

    # Define output and report paths
    report="$OUTPUT_DIR/${base}.report"
    output="$OUTPUT_DIR/${base}.kraken"

    # Run kraken2
    echo "Processing $file..."
    kraken2 --db "$DB" --threads "$THREADS" --report "$report" --output "$output" "$file"
done

echo "All files processed!"

