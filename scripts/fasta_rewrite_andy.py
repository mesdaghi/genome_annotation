def clean_fasta_headers(input_fasta, output_fasta):
    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                # Keep only the part before the first pipe character
                header = line.split('|')[0].strip()
                outfile.write(f"{header}\n")
            else:
                outfile.write(line)

# Example usage:
# Replace with your actual filenames
input_file = "Afumigatus_07_05_24.fasta"
output_file = "Afumigatus_07_05_24_CLEAN.fasta"

clean_fasta_headers(input_file, output_file)

