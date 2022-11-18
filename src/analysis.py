import pandas as pd
import os
import json

class Analyzer:

    def __init__(self):
        self.data_folder = './data/filtered_reports'
        self.tabCount = 0
        self.full_df = pd.DataFrame(columns = ['date', 'time', 'information'])
        self.count = 0

    def pull_reports(self):
        search_phrases = None
        with open('./data/search_phrases.json', 'r') as json_search_phrases:
            output = json.load(json_search_phrases)
            search_phrases = output['keywords']
        for folderName in os.listdir(self.data_folder):
            if folderName != '.gitkeep':
                
                
                for tableName in os.listdir(f'{self.data_folder}/{folderName}'):
                    self.tabCount += 1

                    # Marking places where there are no incidents
                    df = pd.read_csv(f'{self.data_folder}/{folderName}/{tableName}')
                    for keywords in search_phrases:
                        # There has GOT to be a better way to find this, but <isin> doesn't work.
                        for (columnName, columnData) in df.iteritems():
                            for (rowName, rowData) in columnData.iteritems():
                                if isinstance(rowData, str) and keywords['words'] in rowData:
                                    with open(f'./data/json_reports/{folderName}.json', 'r') as outputFile:
                                        outputFile = json.load(outputFile)
                                        outputFile[keywords['phrase']] = None
                                        outputFile = json.dumps(outputFile, indent = 4)
                                        json_file = open(f'./data/json_reports/{folderName}.json', 'w')
                                        json_file.write(outputFile)
                                        json_file.close()
                    
                    # Recording all the incidents
                    
            self.count += 1
            print(f'{(self.count/1332)*100}% complete.')
        #print(self.full_df)

Analayzer = Analyzer()

Analayzer.pull_reports()
