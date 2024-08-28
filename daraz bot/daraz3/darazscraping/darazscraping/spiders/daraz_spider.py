import scrapy
import json
from scrapy.crawler import CrawlerProcess

class DarazSpider(scrapy.Spider):
    name = 'daraz'

    def __init__(self, query='', category='', subcategory=''):
        self.query = query
        self.category = category
        self.subcategory = subcategory

    def start_requests(self):
        base_url = 'https://www.daraz.pk/baby-personal-care/?ajax=true&page={page}&q={query}&spm=a2a0e.home.search.go.73534937nyx1OS'
        for i in range(1, 170):  # Adjust range as needed
            url = base_url.format(page=i, query=self.query)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            resp = json.loads(response.text)
            data = resp.get("mods", {}).get("listItems", [])

            if not data:
                self.logger.info("No data found on page")

            for info in data:
                product_name = info.get('name', 'N/A')
                product_price = info.get('price', 'N/A')
                product_img = info.get('image', 'N/A')
                product_rating = info.get('ratingScore', 'N/A')
                product_reviews_count = info.get('review', 'N/A')
                product_link = info.get('productUrl', 'N/A')

                yield {
                    'name': product_name,
                    'price': product_price,
                    'img': product_img,
                    'rating': product_rating,
                    'reviews_count': product_reviews_count,
                    'link': product_link,
                    'category': self.category,
                    'subcategory': self.subcategory
                }
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON response")
            self.logger.debug(response.text)

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_URI': 'baby-personal-care.csv',
        'FEED_FORMAT': 'csv',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': 'DEBUG'
    })
    process.crawl(DarazSpider, query='all', category='Mother & Baby ', subcategory='baby personal care')
    process.start()
