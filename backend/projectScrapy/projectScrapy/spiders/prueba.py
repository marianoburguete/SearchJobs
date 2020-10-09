import scrapy


class PruebaSpider(scrapy.Spider):
    name = 'prueba'
    allowed_domains = ['www.prueba.com']
    start_urls = ['http://www.prueba.com/']

    def parse(self, response):
        pass
