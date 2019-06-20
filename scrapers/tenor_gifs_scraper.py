import scrapy
import subprocess

class TenorGIFSpider(scrapy.Spider):
    name = "tenor_gifs_spider"

    def __init__(self, search_terms):
        self.count = 0
        self.search_terms = search_terms.split(",")
        self.start_urls = ["https://tenor.com/search/" + self.search_terms[self.count].replace(" ", "-") + "-gifs"] #url to scrape

    def parse(self, response):
        img_urls = []
        img_urls = response.xpath("//img/@src").extract()
        op = ""
        for img_url in img_urls:
            if "media" in img_url and "images" in img_url:
                op = img_url
                break
        print(op)
    
        if(self.count < len(self.search_terms)):
            self.count+=1
            self.start_urls = ["https://tenor.com/search/" + self.search_terms[self.count].replace(" ", "-") + "-gifs"]
            yield scrapy.Request(self.start_urls[0], callback=self.parse, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36"})

def runGIFSpider(search_terms):
    op = subprocess.check_output("scrapy runspider scrapers/tenor_gifs_scraper.py --nolog -a search_terms=" + "\"" + ",".join(search_terms) + "\"", shell=True, universal_newlines=True)
    op = op.split("\n")
    op = [i for i in op if i]
    print(op)
    return op

if __name__ == "__main__":
    runGIFSpider(["melt", "hi", "bye"])