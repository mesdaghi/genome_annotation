import re
import json
from pathlib import Path
from Bio import SeqIO  

def parse_failed_predictions(file_path):
    failed_ids = set()
    all_ids = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        # Capture all predicted identifiers
        if "Saving prediction to" in line:
            match = re.search(r'\./before/([\w\-]+)\.pdb', line)  #line may need editing!
            if match:
                all_ids.append(match.group(1))

        # Capture failed ones
        if "INFO:root:Failed to generate" in line:
            match = re.search(r'\./before/([\w\-]+)\.pdb', line) #line may need editing!
            if match:
                failed_ids.add(match.group(1))

    return failed_ids, all_ids

def generate_json_for_success(fasta_path, failed_ids, output_dir):
    Path(output_dir).mkdir(exist_ok=True)

    for record in SeqIO.parse(fasta_path, "fasta"):
        seq_id = record.id.split()[0]  
        if seq_id not in failed_ids:
            data = [{
                "sequences": [
                    {
                        "proteinChain": {
                            "sequence": str(record.seq),
                            "count": 1
                        }
                    }
                ],
                "name": seq_id
            }]
            out_file = Path(output_dir) / f"{seq_id}.json"
            with open(out_file, "w") as f:
                json.dump(data, f, indent=4)
    print(f"JSON files saved in '{output_dir}'")


log_file = "nohup.txt"  
fasta_file = "before.fasta"  
output_folder = "json_output_before"  

failed, all_ids = parse_failed_predictions(log_file)
generate_json_for_success(fasta_file, failed, output_folder)
