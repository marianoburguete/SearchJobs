from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from projectScrapy.items import CTItem


class WorkanaSpider(CrawlSpider):
    name = 'workana'
    allowed_domains = ['www.workana.com']
    start_urls = ['https://www.workana.com/jobs?country=UY']

    items_count = 0

    rules = (
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='')),
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//*[@id="projects"]/div/div[1]/h2/a'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        it = CTItem()
        it['url'] = response.request.url
        it['title'] = response.xpath('normalize-space(//*[@id="productName"]/h1/text())').get()
        it['workday'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/p[3]/strong[5]/text())').get()
        it['contract_type'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/p[5]/text())').get()
        it['salary'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/div[1]/div[2]/h4/text())').get()
        it['description'] = response.xpath(
            'normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/section/article[1]/div[2])').get()
        it['requirements'] = response.xpath('normalize-space(//p[@class="skills"])')
        it['company_name'] = response.xpath('//*[@id="app"]/div/div[2]/section/section[1]/div/aside/article[3]/div[1]/a/span/text()').get()
        yield it
