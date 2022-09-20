import pandas as pd

df = pd.read_csv('./test-page-1-table-1.csv')
print(df)


# import camelot as cm

# output = cm.read_pdf('./data/raw_reports/00077dc5-c0c0-4cef-97e9-4d07e414db75.pdf', pages = 'all', flavor = 'stream')

# output.export('test.csv', f = 'csv', compress = False)