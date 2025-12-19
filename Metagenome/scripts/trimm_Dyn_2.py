import pandas as pd
import subprocess
import time

start_time = time.time()
# Read CSV without header
list_runs = pd.read_csv('runs.csv', header=None)
size_list = len(list_runs)

# Open a log file to store all outputs
with open("trimmomatic_log.txt", "w") as log_file:
    for i in range(size_list):
        tmp = str(list_runs.iloc[i, 0]).strip()  # Ensure it's a clean string

        command = [
            "java", "-jar", "trimmomatic-0.39.jar",
            "SE", "-phred33",
            rf"D:/breastmilk_Valerie/Metagenome/raw data/fastq/{tmp}.fastq.gz",
            rf"D:/breastmilk_Valerie/Metagenome/raw data/filtered/{tmp}.fastq.gz",
            "ILLUMINACLIP:TruSeq3-SE.fa:2:30:10",
            "LEADING:3",
            "TRAILING:3",
            "SLIDINGWINDOW:4:15",
            "MINLEN:36"
        ]

        # Print the command for debugging
        print(f"Running: {' '.join(command)}")

        try:
            # Capture stdout and stderr and write to log file
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log_file.write(f"=== Output for {tmp} ===\n")
            log_file.write(result.stdout + "\n")
            log_file.write("="*50 + "\n")
            print(f"Trimmomatic executed successfully for {tmp}!")
        except subprocess.CalledProcessError as e:
            log_file.write(f"Error occurred for {tmp}: {e}\n")
            print(f"Error occurred for {tmp}: {e}")

elapsed_time = time.time() - start_time
print("time")
print(elapsed_time)