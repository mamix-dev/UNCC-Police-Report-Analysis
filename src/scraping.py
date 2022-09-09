import requests
from bs4 import BeautifulSoup

class Scraper:
    # Setting up the scraper itself
    def __init__(self):
        source = requests.get('https://police.charlotte.edu/log')
        soup = BeautifulSoup(source.content, 'html.parser')
        self.listContainer = soup.find_all('div', 'field-item even')
        self.fullLinkList = []

    # Collecting all of the links of the elements and adding it to a list
    def collectLinks(self):
        for item in self.listContainer:
            linkElements = item.find_all('a')
            for link in linkElements:
                self.fullLinkList.append(link['href'])

    # Remove unneeded links, complete incomplete links, and save all to .txt file under ./data/links.txt
    def saveCleanLinks(self):
        self.collectLinks()
        linksFile = open('./data/links.txt', 'w')
        for item in self.fullLinkList:
            if item.find('ninertimes') == -1:
                if item[0] == '/':
                    linksFile.write('https://police.charlotte.edu'+item+'\n')
                else:
                    linksFile.write(item+'\n')
        linksFile.close()

if __name__ == '__main__':
    scraper = Scraper()
    scraper.saveCleanLinks()