import re
import matplotlib.pyplot as plt

def parse_failed_predictions(file_path):
    failed_dict = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "INFO:root:Failed to generate" in line:
            # Extract FASTA ID from the file path
            match = re.search(r'\./before/([\w\-]+)\.pdb', line) #may need to change!
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

def plot_histogram(data_dict, output_path='failed_predictions_histogram_before.png'):
    identifiers = list(data_dict.keys())
    lengths = list(data_dict.values())

    plt.figure(figsize=(12, 6))
    plt.bar(identifiers, lengths)
    plt.xlabel('FASTA Identifier')
    plt.ylabel('Sequence Length')
    plt.title('Sequence Lengths of Failed Predictions')
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Histogram saved as '{output_path}'")

# Example usage
file_path = "nohup.txt"  #may need to change!
result = parse_failed_predictions(file_path)

print(f"Total failed predictions: {len(result)}")
if result:
    print(f"Highest sequence length: {max(result.values())}")
    print(f"Lowest sequence length: {min(result.values())}")
    plot_histogram(result)
