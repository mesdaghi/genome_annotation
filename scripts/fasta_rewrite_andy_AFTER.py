def rewrite_fasta_headers_by_name(input_fasta, output_fasta):
    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                # Extract the name= value from the header
                parts = line.strip().split()
                name_part = [part for part in parts if part.startswith("name=")]
                if name_part:
                    name = name_part[0].split("=", 1)[1]
                    outfile.write(f">{name}\n")
                else:
                    # Fallback: write original header if 'name=' is missing
                    outfile.write(line)
            else:
                outfile.write(line)

# Example usage
input_file = "Afumigatus_07_05_24.fasta"
output_file = "Afumigatus_07_05_24_CLEAN.fasta"
rewrite_fasta_headers_by_name(input_file, output_file)

