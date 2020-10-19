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
            'normalize-space(//section[@class="box box_r"]//li[h3[contains(text(), "Localización")]]//p/text())').get()
        it['workday'] = response.xpath(
            'normalize-space(//section[@class="box box_r"]//li[h3[contains(text(), "Jornada")]]//p/text())').get()
        it['contract_type'] = response.xpath(
            'normalize-space(//section[@class="box box_r"]//li[h3[contains(text(), "Tipo de contrato")]]//p/text())').get()
        it['salary'] = response.xpath(
            'normalize-space(//section[@class="box box_r"]//li[h3[contains(text(), "Salario")]]//p/text())').get()
        it['description'] = response.xpath(
            'normalize-space(//div[@class="cm-12 box_i bWord"]//li[2])').get()
        requirements = []
        for li in response.xpath('//div[@class="cm-12 box_i bWord"]//li/text()').getall():
            if 'Edad:' in li or 'Educación Mínima:' in li or 'Edad:' in li or 'Disponibilidad de Viajar:' in li or 'Disponibilidad de Cambio de Residencia:' in li:
                requirements.append(li)
        it['requirements'] = requirements.copy()
        it['company_name'] = response.xpath('//*[@id="MainContainer"]/article/section[1]/div[1]/div/h2/text()').get()
        it['company_logo'] = response.xpath('//div[@class="cm-3 detalle_logoempresa"]/img/@src').get()
        it['category'] = response.xpath('//ol//li[3]//text()').get()
        yield it
