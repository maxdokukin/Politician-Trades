import os
import pandas as pd

# Specify the directory containing your CSV files
csv_dir = 'data/Scrapes Combined/'
output_file = 'data/all_combined.csv'

import re

file_names = os.listdir(csv_dir)
def extract_number(file_name):
    match = re.search(r'\d+', file_name)
    return int(match.group()) if match else 0

# Sort file names using the extracted numbers
sorted_file_names = sorted(file_names, key=extract_number, reverse=True)

# Check if the output file already exists, and if so, remove it
if os.path.exists(output_file):
    os.remove(output_file)

# Loop through all files in the directory
for file in sorted_file_names:
    if file.endswith('.csv'):
        # Construct full file path
        file_path = os.path.join(csv_dir, file)
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)

        # If the output file doesn't exist, write with the header, else append without the header
        if not os.path.exists(output_file):
            df.to_csv(output_file, mode='w', index=False, header=False)
        else:
            df.to_csv(output_file, mode='a', index=False, header=False)

        print(f'Appended {file_path} to {output_file}', df.shape[0], ' entries')

print(f'All CSV files have been combined into {output_file}')
