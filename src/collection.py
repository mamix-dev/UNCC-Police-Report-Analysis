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
            txt_report.write((fullText).encode('utf8'))

# Iterates through text files and extracts data of import
def extractData():
    count = 0
    for report_name in os.listdir('./data/txt_reports'):
        tup = report_name.split('.')
        ext = tup[1]
        name = tup[0]
        if ext == 'txt':
            count += 1
            fileStream = open(f'./data/txt_reports/{report_name}', 'rb')
            date_found = False
            json_contents = {}
            # Iterate through all lines in text files
            for line in fileStream.readlines():
                line = line.decode('utf8')
                # Finding the date
                if not date_found:
                    date = dparser.parse(line)
                    if date != None:
                        json_contents['date'] = str(date-datetime.timedelta(days=1))
                        date_found = True
                list_of_words = line.split()
                # Finding total calls
                total_call_phrase_words = ['CALLS', 'FOR', 'SERVICE']
                if all(word in list_of_words for word in total_call_phrase_words):
                    for word in list_of_words:
                        if word.isdigit():
                            json_contents['total_calls'] = int(word)
                
            # Writing extracted data to a .json under ./data/json_reports/
            json_object = json.dumps(json_contents, indent = 4)
            json_file = open(f'./data/json_reports/{name}.json', 'w')
            json_file.write(json_object)
            json_file.close()
        print(f'{(count/1332)*100}% complete.')



extractData()