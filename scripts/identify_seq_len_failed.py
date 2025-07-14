import re

def parse_failed_predictions(file_path):
    failed_dict = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "INFO:root:Failed to generate" in line:
            # Extract FASTA ID from the file path
            match = re.search(r'\./after/([\w\-]+)\.pdb', line)
            if match:
                fasta_id = match.group(1)

                # Look backward for the most recent "residues in this chain" line
                for j in range(i - 1, -1, -1):
                    if "residues in this chain." in lines[j]:
                        res_match = re.search(r'INFO:root:(\d+)\s+residues in this chain\.', lines[j])
                        if res_match:
                            residue_count = int(res_match.group(1))
                            failed_dict[fasta_id] = residue_count
                        break

    return failed_dict

file_path = "nohup2.txt"  
result = parse_failed_predictions(file_path)

print(f"Total failed predictions: {len(result)}")
if result:
    print(f"Highest sequence length: {max(result.values())}")
    print(f"Lowest sequence length: {min(result.values())}")


