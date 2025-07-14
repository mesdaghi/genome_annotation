
import re

# Input paths
log_file = "nohup2.txt"
fasta_file = "Afumigatus_07_05_24_CLEAN.fasta"
output_fasta = "failed_sequences_after.fasta"

# Step 1: Extract failed prediction IDs
failed_ids = []

with open(log_file, "r") as file:
    for line in file:
        if "INFO:root:Failed to generate" in line:
            match = re.search(r'./after/(.+?)\.pdb', line)
            if match:
                failed_ids.append(match.group(1))

# Step 2: Read FASTA and extract matching sequences
write = False
with open(fasta_file, "r") as infile, open(output_fasta, "w") as outfile:
    for line in infile:
        if line.startswith(">"):
            fasta_id = line[1:].strip()
            write = fasta_id in failed_ids
        if write:
            outfile.write(line)

print(f"Saved {len(failed_ids)} failed sequences to {output_fasta}")
