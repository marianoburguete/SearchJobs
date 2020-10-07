from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from projectScrapy.items import WOItem
import scrapy



class WorkanaSpider(CrawlSpider):
    name = 'workana'
    allowed_domains = ['www.workana.com']
    start_urls = ['https://www.workana.com/jobs?country=UY']

    items_count = 0
    page_count = 2

    rules = (
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//ul[@class="pagination"]//li//a[contains(text(),' + f'{page_count}' + ')]'),
            callback='func',
            follow=True),
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//*[@id="projects"]/div/div[1]/h2/a'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        # if self.items_count > 1000:
        #     raise CloseSpider('items exceeded')
        # self.items_count += 1


        it = WOItem()
        it['url'] = response.request.url
        it['title'] = response.xpath('normalize-space(//*[@id="productName"]/h1/text())').get()
        it['workday'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div/section/section/div/section/article/p/strong[5]//text())').get()
        it['contract_type'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/p[5]/text())').get()
        it['salary'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/div[1]/div[2]/h4/text())').get()
        it['description'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/div[2]/text())').get()
        it['requirements'] = response.xpath('normalize-space(//p[@class="skills"]//text())').get()
        it['company_name'] = response.xpath('//*[@id="app"]/div/div[2]/section/section[1]/div/aside/article[3]/div[1]/a/span/text()').get()
        it['prueba'] = response.xpath('//p[@class="resume"]').get()

        
        #next_url = response.xpath('//ul[@class="pagination"]//li//a[contains(text(),' + self.page_count + ')]/@href') #response.css('#pagination > ul > li > a[href~="?page={0}"]::attr(href)'.format(self.page_count))
        
        yield it
        # if next_url:
        #     yield scrapy.Request(
        #         url = next_url
        #     )
        
    def func(self, response):
        self.page_count += 1
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
