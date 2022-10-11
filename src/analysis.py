import pandas as pd
import os

class Analyzer:

    def __init__(self):
        self.data_folder = './data/filtered_reports'
        self.tabCount = 0
        self.full_df = pd.DataFrame(columns = ['date', 'time', 'information'])

    def pull_reports(self):
        for folderName in os.listdir(self.data_folder):
            if folderName != '.gitkeep':
                for tableName in os.listdir(f'{self.data_folder}/{folderName}'):
                    self.tabCount += 1
                    df = pd.read_csv(f'{self.data_folder}/{folderName}/{tableName}')
        print(f'{self.tabCount} tables were found.')
        print(self.full_df)

Analayzer = Analyzer()

Analayzer.pull_reports()