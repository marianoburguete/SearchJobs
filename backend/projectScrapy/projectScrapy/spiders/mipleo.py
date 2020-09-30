from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from projectScrapy.items import MTItem


class MipleoSpider(CrawlSpider):
    name = 'mipleo'
    allowed_domains = ['uy.mipleo.com']
    start_urls = ['https://uy.mipleo.com/ofertas-de-trabajo/?pag=1']

    items_count = 0

    rules = ( 
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//*[@id="pages"]/a[contains(text(), ">")]')),
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//span[@class="titleAd"]'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        # if self.items_count > 20:
        #     raise CloseSpider('items exceeded')
        # self.items_count += 1
        it = MTItem()
        it['url'] = response.request.url
        it['title'] = response.xpath('normalize-space(//h1/text())').get()
        it['location'] = response.xpath(
            '//*[@id="content"]/div[3]/div[2]/ul/li[4]/b/text()').get()
        it['workday'] = response.xpath(
            '//*[@id="content"]/div[3]/div[2]/ul/li[6]/b/text()').get()
        it['contract_type'] = response.xpath(
            '//*[@id="content"]/div[3]/div[2]/ul/li[7]/b/text()').get()
        it['salary'] = response.xpath(
            '//*[@id="content"]/div[3]/div[2]/ul/li[1]/b/text()').get()
        it['description'] = response.xpath(
            '//*[@id="content"]/div[3]/div[2]/div[2]/p/text()').get()
        requirements = []
        for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul/li').getall():
            print("PRUEBA: " + str(type(ul)) )
            prueba = ul.xpath("text()").getall()
            for index, x in prueba:
                requirements.append(x)
            
        it['requirements'] = requirements.copy()
        it['company_name'] = response.xpath('//*[@id="content"]/div[4]/div[1]/span/text()').get()
        yield it

        #for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul/text()').getall():
        #for ul in response.xpath('//ul[@class="info_item"]//li/text()').getall():