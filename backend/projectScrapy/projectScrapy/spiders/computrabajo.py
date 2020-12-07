from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from projectScrapy.items import CTItem


class ComputrabajoSpider(CrawlSpider):
    name = 'computrabajo'
    allowed_domains = ['www.computrabajo.com.uy']
    start_urls = ['https://www.computrabajo.com.uy/ofertas-de-trabajo/']

    items_count = 0

    rules = (
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//li[@class="siguiente"]')),
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//a[@class="js-o-link"]'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        # if self.items_count > 20:
        #     raise CloseSpider('items exceeded')
        # self.items_count += 1
        it = CTItem()
        it['url'] = response.request.url
        it['title'] = response.xpath('normalize-space(//h1/text())').get()
        it['location'] = response.xpath(
            'normalize-space(//section[@class="boxWhite fl w_100 ocultar_mvl p30"]//li[2])').get()
        it['workday'] = response.xpath(
            'normalize-space(//section[@class="boxWhite fl w_100 ocultar_mvl p30"]//li[p[contains(text(), "Jornada")]])').get().replace('Jornada ', '')
        it['contract_type'] = response.xpath(
            'normalize-space(//section[@class="boxWhite fl w_100 ocultar_mvl p30"]//li[p[contains(text(), "Tipo de contrato")]])').get().replace('Tipo de contrato ', '')
        it['salary'] = response.xpath(
            'normalize-space(//section[@class="boxWhite fl w_100 ocultar_mvl p30"]//li[p[contains(text(), "Salario")]])').get().replace('Salario ', '')
        it['description'] = response.xpath(
            'normalize-space(//ul[@class="p0 m0"]//li[2])').get()
        requirements = []
        for li in response.xpath('//ul[@class="p0 m0"]//li/text()').getall():
            if 'Edad:' in li or 'Educación Mínima:' in li or 'Edad:' in li or 'Disponibilidad de Viajar:' in li or 'Disponibilidad de Cambio de Residencia:' in li:
                requirements.append(li)
        it['requirements'] = requirements.copy()
        it['company_name'] = response.xpath('//*[@id="MainContainer"]//article[1]//a[@id="urlverofertas"]/text()').get()
        it['company_logo'] = response.xpath('//div[@class="logo_empresa ocultar_mvl"]/img/@src').get()
        it['category'] = response.xpath('//ol//li[3]//text()').get()
        yield it
