import pandas as pd
import subprocess
import time
import os

start_time = time.time()

# ---- CONFIGURE THESE PATHS ----
TRIM_JAR = r"trimmomatic-0.39.jar"
ADAPTERS = r"TruSeq3-PE.fa"  # PE adapter file
IN_DIR = r"D:/breastmilk_Valerie/Metagenome/raw data/fastq"
OUT_DIR = r"D:/breastmilk_Valerie/Metagenome/raw data/filtered"
RUNS_CSV = "runs.csv"  # one sample ID per line (no header)
PHRED = "-phred33"

# Create output directory if missing
os.makedirs(OUT_DIR, exist_ok=True)

# Read CSV without header
list_runs = pd.read_csv(RUNS_CSV, header=None)
size_list = len(list_runs)

log_path = "trimmomatic_pe_log.txt"
with open(log_path, "w", encoding="utf-8") as log_file:
    for i in range(size_list):
        sample = str(list_runs.iloc[i, 0]).strip()

        # Input files: sample_R1.fastq.gz and sample_R2.fastq.gz
        r1_in = rf"{IN_DIR}/{sample}_1.fastq.gz"
        r2_in = rf"{IN_DIR}/{sample}_2.fastq.gz"

        # Output files:
        r1_paired = rf"{OUT_DIR}/{sample}_1.paired.fastq.gz"
        r1_unpaired = rf"{OUT_DIR}/{sample}_1.unpaired.fastq.gz"
        r2_paired = rf"{OUT_DIR}/{sample}_2.paired.fastq.gz"
        r2_unpaired = rf"{OUT_DIR}/{sample}_2.unpaired.fastq.gz"

        # Trimmomatic PE command
        command = [
            "java", "-jar", TRIM_JAR,
            "PE", PHRED,
            r1_in, r2_in,
            r1_paired, r1_unpaired,
            r2_paired, r2_unpaired,
            f"ILLUMINACLIP:TruSeq3-PE.fa:2:30:10",
            "LEADING:3",
            "TRAILING:3",
            "SLIDINGWINDOW:4:15",
            "MINLEN:36"
        ]

        # Print command for debugging
        print(f"Running: {' '.join(command)}")

        # Check input files exist before running
        missing = [p for p in (r1_in, r2_in) if not os.path.isfile(p)]
        if missing:
            msg = f"[SKIP] {sample} missing files: {', '.join(missing)}\n"
            log_file.write(msg)
            print(msg.strip())
            continue

        try:
            # Capture stdout and stderr and write to log file
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True
            )
            log_file.write(f"=== Output for {sample} ===\n")
            log_file.write(result.stdout + "\n")
            log_file.write("=" * 50 + "\n")
            print(f"Trimmomatic PE executed successfully for {sample}!")
        except subprocess.CalledProcessError as e:
            log_file.write(f"[ERROR] {sample}: return code {e.returncode}\n")
            log_file.write(e.stdout if e.stdout else "" + "\n")
            print(f"Error occurred for {sample}: {e}")

elapsed_time = time.time() - start_time
print("Total runtime (seconds):", round(elapsed_time, 2))
