from io import StringIO
import uuid
import requests
import os
from PyPDF2 import PdfFileReader
import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

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
    for reportName in os.listdir('./data/raw_reports'):
        tup = reportName.split('.')
        ext = tup[1]
        name = tup[0]
        if ext == 'pdf':
            stream = open(f'./data/raw_reports/{reportName}', 'rb')
            reader = PdfFileReader(stream)
            fullText = ''
            for pageNum in range(reader.numPages):
                raw_text = reader.getPage(pageNum).extract_text()
                fullText += ('\n' + raw_text + '\n')
            txt_report = open(f'./data/txt_reports/{name}.txt', 'wb')
            txt_report.write((fullText).encode('utf8'))

# def extractText():
#     output_string = StringIO()
#     for reportName in os.listdir('./data/raw_reports'):
#         tup = reportName.split('.')
#         ext = tup[1]
#         name = tup[0]
#         if ext == 'pdf':
#             with open(f'./data/raw_reports/{reportName}', 'rb') as in_file:
#                     parser = PDFParser(in_file)
#                     doc = PDFDocument(parser)
#                     rsrcmgr = PDFResourceManager()
#                     device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
#                     interpreter = PDFPageInterpreter(rsrcmgr, device)
#                     for page in PDFPage.create_pages(doc):
#                         interpreter.process_page(page)
#                     txt_report = open(f'./data/txt_reports/{name}.txt', 'wb')
#                     txt_report.write((output_string.getvalue()).encode('utf8'))

# extractText()

def checkForPhrase(phrase):
    count = 0
    for reportName in os.listdir('./data/txt_reports'):
        tup = reportName.split('.')
        ext = tup[1]
        if ext == 'txt':
            fileStream = open(f'./data/txt_reports/{reportName}', 'rb')
            hasPhrase = False
            for line in fileStream.readlines():
                line = line.decode('utf8')
                if line.find(phrase) != -1:
                    hasPhrase = True
                    print(line)
                    count += 1
    print(count)


checkForPhrase('  ')