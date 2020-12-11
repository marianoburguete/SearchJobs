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
            'normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Localidad")]/b/text())').get()
        it['workday'] = response.xpath(
            'normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Jornada")]/b/text())').get()
        it['contract_type'] = response.xpath(
            'normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Tipo de Contrato")]/b/text())').get()
        it['salary'] = response.xpath(
            'normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Salario")]/b/text())').get()
        it['description'] = response.xpath(
            'normalize-space(//*[@id="content"]/div[3]/div[2]/div[2]/p/text())').get()
        requirements = []
        for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul//li//text()').getall():
            if 'Idiomas:' in ul:
                requirements.append(response.xpath('normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Idiomas")])').get())
        for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul//li//text()').getall():
            if 'Disponibilidad de cambio de residencia:' in ul:
                requirements.append(response.xpath('normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Disponibilidad de cambio de residencia:")])').get())
        for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul//li//text()').getall():
            if 'Disponibilidad de viajar:' in ul:
                requirements.append(response.xpath('normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Disponibilidad de viajar:")])').get())
        for ul in response.xpath('//*[@id="content"]/div[3]/div[2]/ul//li//text()').getall():
            if 'Educación Mínima:' in ul:
                requirements.append(response.xpath('normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Educación Mínima:")])').get())           
        it['requirements'] = requirements.copy()
        it['company_name'] = response.xpath('//*[@id="content"]/div[4]/div[1]/span[1]/text()').get()
        it['category'] = response.xpath('normalize-space(//*[@id="content"]/div[3]/div[2]/ul/li[contains(text(), "Categoría")]/b/text())').get()
        yield it
