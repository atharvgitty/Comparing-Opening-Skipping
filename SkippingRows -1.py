#run if comparison doesn't work	and then run comparison after adding this code
#if used, only specify column number, as rows will be skipped 
#skipping initial rows like qgc_something_something and the header row
import os
import csv

# directory containing CSV files
directory = '/path/to/csv/files'

# number of rows to skip
skip_rows = 2

# loop through CSV files in directory and skip rows
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i < skip_rows:  # skip rows
                    continue