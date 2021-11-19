import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv


class LotItem:
    def __init__(self, lotNumber, title, currentPrice, numberOfBids, url):
        self.lotNumber = lotNumber
        self.title = title
        self.currentPrice = currentPrice
        self.numberOfBids = numberOfBids
        self.url = url

    def print(self):
        print("LOT: " + lotNumber + " TITLE: " + title + " CURRENT PRICE: " +
              currentPrice + " NUMBER OF BIDS: " + numberOfBids + " URL: " + url)


def writeToFile(csvItems):
    with open('data.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lot Number', 'Name', 'Current Price',
                        'Number of Bids', 'Link'])
        for item in csvItems:
            writer.writerow([item.lotNumber, item.title,
                            item.currentPrice, item.numberOfBids, item.url])


def getItemInfoInCsvList(listingItems):
    csvItems = []
    for item in listingItems:
        lotNumber = item.find("a", class_='btn-bid')['data-lot-id']
        title = item.find("p", class_='item-title').getText()
        currentPrice = item.find("p", class_='item-current-bid').getText()
        numberOfBids = item.find("span", class_='item-bid-count').getText()
        url = "https://bid.liquidbidding.com/lots/" + lotNumber
        csvItems.append(
            LotItem(lotNumber, title, currentPrice, numberOfBids, url))
    return csvItems


driver = webdriver.Firefox()
listingItems = []
mainUrl = "https://bid.liquidbidding.com/lots#YXVjdGlvbltpZF09NjUyMyZhdWN0aW9uW2xvY2F0aW9uXT1hbGwmYXVjdGlvbltzdGF0dXNdPXVwY29taW5nJmF1Y3Rpb25bdHlwZV09YWxsJmxpbWl0PTE1MCZsb3RbY2F0ZWdvcnldPWFsbCZsb3RbbG9jYXRpb25dPWFsbCZsb3RbbWlsZV9yYWRpdXNdPTI1JnBhZ2U9MQ.."

driver.get(mainUrl)
# todo: make this a smart wait by waiting for exact elements to finish loading
time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")

listingItems += soup.find_all("div", class_='item-lot')

csvItems = getItemInfoInCsvList(listingItems)


driver.close()
writeToFile(csvItems)
