import scrapy
import urllib.request
import csv
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import os

class ImageSpider(scrapy.Spider):
    name = "image_spider"
    # wordlist = []
    # with open("wordlist.csv", "r") as csvfile:
    #     readCSV = csv.reader(csvfile)
    #     for row in readCSV:
    #         wordlist += row


    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    def __init__(self, search_term):
        self.search_term = search_term
        self.count = 0
        self.start_urls = ["https://www.google.co.in/search?q=" + search_term + "&tbm=isch"]

    def parse(self, response):
        print("NOW SEARCHING: " + self.search_term)
        img_urls = []
        # img_count = 0
        # for imagecolumn in response.css(".photos__column"):#response.xpath("//div[@class=\"photos__column\"]"):
        #     if(not imagecolumn.xpath(".//a[@class=\"js-photo-link photo-item__link\"]")):
        #         break
        #     img_url = (imagecolumn.xpath(".//a[@class=\"js-photo-link photo-item__link\"]/img/@data-big-src").extract_first())#.replace(".jpeg", ".jpg").split(".jpg")[0] + ".jpg"
        #     img_count += 1
        #     yield {
        #         "image": img_url
        #     }
        #     urllib.request.urlretrieve(img_url, "Images/" + self.wordlist[ImageSpider.count] + " " + str(img_count) + ".jpg")
        
        img_urls = response.xpath("//img/@src").extract()
        for i in range(0, 1):
            print("static/uploads/" + self.search_term + " " + str(i) + ".jpg")
            urllib.request.urlretrieve(img_urls[i], "static/uploads/" + self.search_term + " " + str(i) + ".jpg")


        # if(ImageSpider.count < len(self.wordlist)):
        #     ImageSpider.count += 1
        #     yield scrapy.Request(response.urljoin(
        #         "https://www.google.co.in/search?q=" + self.wordlist[ImageSpider.count] + "&tbm=isch"),
        #         callback=self.parse, dont_filter=True)

def runSpider(search_term):
    os.system("scrapy runspider google_images_scraper.py  -a search_term=" + '"' + str(search_term) + '"')
    # process = CrawlerProcess({
    #     'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    # })
    # process = CrawlerProcess()
    # process = CrawlerRunner()
    # process.crawl(ImageSpider, search_term=search_term)
    # process.start()
    # reactor.run()


if __name__ == "__main__":
    runSpider("jam")