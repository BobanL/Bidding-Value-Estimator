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


def getAllListingItems(soup):
    listingItems = []
    # todo: figure out what happens if there are no pages
    pageLength = soup.find("ul", class_="pagination pull-right").find_all("li")

    lastPage = int(pageLength[len(pageLength) - 2].a.getText())
    currentPage = int(soup.find("li", class_="active").a.getText())

    while currentPage < lastPage:
        # todo: handle modal popup
        # todo: wait for page to load
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        listingItems += soup.find_all("div", class_='item-lot')
        driver.find_element(
            by="css selector", value="#lot_listing > div:nth-child(4) > div > div.col-sm-7 > ul > li:nth-child(9)").click()
        currentPage += 1

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listingItems += soup.find_all("div", class_='item-lot')
    return listingItems


driver = webdriver.Firefox()
mainUrl = "https://bid.liquidbidding.com/lots#YXVjdGlvbltpZF09NjUyMyZhdWN0aW9uW2xvY2F0aW9uXT1hbGwmYXVjdGlvbltzdGF0dXNdPXVwY29taW5nJmF1Y3Rpb25bdHlwZV09YWxsJmxpbWl0PTE1MCZsb3RbY2F0ZWdvcnldPWFsbCZsb3RbbG9jYXRpb25dPWFsbCZsb3RbbWlsZV9yYWRpdXNdPTI1JnBhZ2U9MQ.."
driver.get(mainUrl)
# todo: make this a smart wait by waiting for exact elements to finish loading
time.sleep(2)
soup = BeautifulSoup(driver.page_source, "html.parser")

listingItems = getAllListingItems(soup)
csvItems = getItemInfoInCsvList(listingItems)

driver.close()
writeToFile(csvItems)
