import camelot as cm
import os

class Exporter:

    def __init__(self):
        self.bugged_tables_counter = 0

    # Creates folders for the reports
    def create_folders(self):
        for filename in os.listdir('./data/raw_reports'):
            if filename != '.gitkeep':
                tup = filename.split('.')
                name = tup[0]
                os.mkdir(f'./data/filtered_reports/{name}')

    def pdf_to_csv(self):
        for filename in os.listdir('./data/raw_reports'):
            if filename != '.gitkeep':
                tup = filename.split('.')
                name = tup[0]
                try:
                    tables = cm.read_pdf(f'./data/raw_reports/{filename}', pages = 'all', flavor = 'stream')
                    tables.export(f'./data/filtered_reports/{name + "/" + name + ".csv"}')
                except Exception as e:
                    print(e)
                    self.bugged_tables_counter += 1
        print(f'{self.bugged_tables_counter} tables were bugged.')

    def export(self):
        first_name = None
        for filename in os.listdir('./data/raw_reports'):
            if filename != '.gitkeep':
                first_name = filename
                break
        # Make folders in case they don't exist.
        name = first_name.split('.')[0]
        if not os.path.isdir(f'./data/filtered_reports/{name}'):
            print('No folders found, creating folders.')
            self.create_folders()
        else:
            print('Folders found, not creating folders.')
        self.pdf_to_csv()

exporter = Exporter()

exporter.export()