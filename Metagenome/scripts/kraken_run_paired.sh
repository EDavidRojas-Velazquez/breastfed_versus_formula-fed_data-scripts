#!/bin/bash

# Define paths
DB="/home/david/kraken_db"
IN_DIR="/home/david/kraken_experiments/filtered"
OUT_DIR="/home/david/kraken_experiments/kraken_rep"

for R1 in "$IN_DIR"/*_1.paired.fastq.gz; do
    R2="${R1/_1.paired.fastq.gz/_2.paired.fastq.gz}"
    sample=$(basename "$R1" | sed 's/_1.paired.fastq.gz//')
    kraken2 --db "$DB" --paired "$R1" "$R2" \
            --threads 20 \
            --report "$OUT_DIR/${sample}.report" \
            --output "$OUT_DIR/${sample}.kraken"
done

