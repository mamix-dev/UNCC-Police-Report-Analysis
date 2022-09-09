import uuid
import requests
import os
from PyPDF2 import PdfFileReader

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

def extractText():
    for reportName in os.listdir('./data/raw_reports'):
        temp = open(f'./data/raw_reports/{reportName}', 'rb')
        pdfRead = PdfFileReader(temp)
        for page in pdfRead.pages:
            print(page.extract_text())
        
        break

downloadFiles()