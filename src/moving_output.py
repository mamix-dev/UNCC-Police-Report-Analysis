import os

for filename in os.listdir('./data/raw_reports'):
    tup = filename.split('.')
    ext = tup[1]
    if ext == 'csv':
        os.replace(f'./data/raw_reports/{filename}', f'./data/filtered_reports/{filename}')