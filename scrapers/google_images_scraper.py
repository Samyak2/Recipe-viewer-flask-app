import scrapy
import urllib.request
import csv
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import os
import subprocess

#spider class (extends scrapy.Spider)
class ImageSpider(scrapy.Spider):
    name = "image_spider" #name of spider

    #to set user agent so that images can be downloaded without being blocked
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    def __init__(self, search_term):
        self.search_term = search_term #set search term
        self.count = 0 #to allow downloading of multiple images
        self.start_urls = ["https://www.google.co.in/search?q=" + search_term + "&tbm=isch"] #set url to scrape

    def parse(self, response):
        print("NOW SEARCHING: " + self.search_term)
        img_urls = response.xpath("//img/@src").extract() #extracts url from all images present
        for i in range(0, 1):
            print("static/uploads/" + self.search_term + " " + str(i) + ".jpg")
            #download image and save it
            urllib.request.urlretrieve(img_urls[i], "static/uploads/" + self.search_term + " " + str(i) + ".jpg")


def runSpider(search_term):
    #runs spider from command line
    if not os.path.isfile("static/uploads/" + search_term + " 0" + ".jpg"):
        # os.system("scrapy runspider google_images_scraper.py  -a search_term=" + '"' + str(search_term) + '"')
        subprocess.Popen(["scrapy", "runspider", "scrapers/google_images_scraper.py",  "-a", "search_term=" + str(search_term)])

#for testing
if __name__ == "__main__":
    runSpider("jam")