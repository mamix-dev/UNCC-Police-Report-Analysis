import dateparser as dparser
import datetime
import uuid
import requests
import os
from PyPDF2 import PdfFileReader
import json

# Downloads the pdfs from the website using the links provided by the links.txt file. PDFs go to ./data/raw_reports/
def downloadFiles():
    count = 0
    linkList = open('./data/links.txt')
    for link in linkList:
        response = requests.get(link.strip(), stream = True)
        with open(f'./data/raw_reports/{uuid.uuid4()}.pdf', 'wb') as fd:
            for chunk in response.iter_content(2000):
                fd.write(chunk)
        count += 1
        print(f'{count}/1332 files downloaded. {(count/1332)*100}% complete.')

# Extracts the data from the PDFs and sends them to a text file.
def extractText():
    for report_name in os.listdir('./data/raw_reports'):
        tup = report_name.split('.')
        ext = tup[1]
        name = tup[0]
        if ext == 'pdf':
            stream = open(f'./data/raw_reports/{report_name}', 'rb')
            reader = PdfFileReader(stream)
            fullText = ''
            for pageNum in range(reader.numPages):
                raw_text = reader.getPage(pageNum).extract_text()
                fullText += ('\n' + raw_text + '\n')
            txt_report = open(f'./data/txt_reports/{name}.txt', 'wb')
            txt_report.write((fullText).encode('UTF-8'))

# Iterates through text files and extracts data of import
def extractData():
    count = 0
    # Getting search phrases out
    search_phrases = None
    with open('./data/search_phrases.json', 'r') as json_search_phrases:
        output = json.load(json_search_phrases)
        search_phrases = output['phrases']
    # Iterate through all text reports
    for report_name in os.listdir('./data/txt_reports'):
        tup = report_name.split('.')
        ext = tup[1]
        name = tup[0]
        # Make sure we don't pick up the .gitignore
        if ext == 'txt':
            count += 1
            fileStream = open(f'./data/txt_reports/{report_name}', 'rb')
            date_found = False
            json_contents = {}
            # Iterate through all lines in text files
            all_lines = fileStream.readlines()
            for line in all_lines:
                line = line.decode('utf8')
                # Finding the date
                if not date_found:
                    date = dparser.parse(line)
                    if date != None:
                        # The first date on the file is the day it is posted, but the day it is posted is the day after the events of the report take place
                        json_contents['date'] = str(date-datetime.timedelta(days=1))
                        date_found = True
                list_of_words = line.split()
                # Finding phrases
                for obj in search_phrases:    
                    phrase_words = obj['words']
                    if all(word in list_of_words for word in phrase_words):
                        for word in list_of_words:
                            if word.isdigit():
                                json_contents[obj['phrase']] = int(word)
                # Pulling out the incidents from the reports
                for idx, word in enumerate(list_of_words):
                    if word == 'INCIDENT' and idx == 0 and len(list_of_words) != 0:
                        print(line)
            # Writing extracted data to a .json under ./data/json_reports/
            json_object = json.dumps(json_contents, indent = 4)
            json_file = open(f'./data/json_reports/{name}.json', 'w')
            json_file.write(json_object)
            json_file.close()
        print(f'{(count/1332)*100}% complete.')



extractData()