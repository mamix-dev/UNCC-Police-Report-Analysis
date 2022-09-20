import os

# Note that this file was made because the output from tabula
# was placed into the ./data/raw_reports and it had to be moved.
for filename in os.listdir('./data/raw_reports'):
    tup = filename.split('.')
    ext = tup[1]
    if ext == 'csv':
        os.replace(f'./data/raw_reports/{filename}', f'./data/filtered_reports/{filename}')