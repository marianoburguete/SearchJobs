import scrapy
from projectScrapy.items import WOItem
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

def extract(raw_string, start_marker, end_marker):
    try:
        start = raw_string.index(start_marker) + len(start_marker)
        end = raw_string.index(end_marker, start)
        return raw_string[start:end]
    except:
        return 'VACIO'

class WorkanaSpider(CrawlSpider):
    name = 'workana'
    allowed_domains = ['www.workana.com']
    # start_urls = [
    # 'https://www.workana.com/jobs?country=UY','https://www.workana.com/jobs?country=UY&page=2','https://www.workana.com/jobs?country=UY&page=3','https://www.workana.com/jobs?country=UY&page=4','https://www.workana.com/jobs?country=UY&page=5','https://www.workana.com/jobs?country=UY&page=6','https://www.workana.com/jobs?country=UY&page=7','https://www.workana.com/jobs?country=UY&page=8','https://www.workana.com/jobs?country=UY&page=9','https://www.workana.com/jobs?country=UY&page=10',
    # 'https://www.workana.com/jobs?country=UY&page=11','https://www.workana.com/jobs?country=UY&page=12','https://www.workana.com/jobs?country=UY&page=13','https://www.workana.com/jobs?country=UY&page=14','https://www.workana.com/jobs?country=UY&page=15','https://www.workana.com/jobs?country=UY&page=16','https://www.workana.com/jobs?country=UY&page=17','https://www.workana.com/jobs?country=UY&page=18','https://www.workana.com/jobs?country=UY&page=19','https://www.workana.com/jobs?country=UY&page=20',
    # 'https://www.workana.com/jobs?country=UY&page=21','https://www.workana.com/jobs?country=UY&page=22','https://www.workana.com/jobs?country=UY&page=23','https://www.workana.com/jobs?country=UY&page=24','https://www.workana.com/jobs?country=UY&page=25','https://www.workana.com/jobs?country=UY&page=26','https://www.workana.com/jobs?country=UY&page=27','https://www.workana.com/jobs?country=UY&page=28','https://www.workana.com/jobs?country=UY&page=29','https://www.workana.com/jobs?country=UY&page=30',
    # 'https://www.workana.com/jobs?country=UY&page=31','https://www.workana.com/jobs?country=UY&page=32','https://www.workana.com/jobs?country=UY&page=33','https://www.workana.com/jobs?country=UY&page=34','https://www.workana.com/jobs?country=UY&page=35','https://www.workana.com/jobs?country=UY&page=36','https://www.workana.com/jobs?country=UY&page=37','https://www.workana.com/jobs?country=UY&page=38','https://www.workana.com/jobs?country=UY&page=39','https://www.workana.com/jobs?country=UY&page=40',
    # 'https://www.workana.com/jobs?country=UY&page=41','https://www.workana.com/jobs?country=UY&page=42','https://www.workana.com/jobs?country=UY&page=43','https://www.workana.com/jobs?country=UY&page=44','https://www.workana.com/jobs?country=UY&page=45','https://www.workana.com/jobs?country=UY&page=46','https://www.workana.com/jobs?country=UY&page=47','https://www.workana.com/jobs?country=UY&page=48','https://www.workana.com/jobs?country=UY&page=49','https://www.workana.com/jobs?country=UY&page=50',
    # ]
    start_urls = [
        'https://www.workana.com/jobs?country=UY'
    ]

    rules = (
        Rule(LinkExtractor(
            allow=(), restrict_xpaths='//*[@id="projects"]/div/div[1]/h2/a'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):
        fields = response.xpath('//p[@class="resume"]').get() 
        it = WOItem()
        it['url'] = response.request.url
        it['title'] = response.xpath('normalize-space(//*[@id="productName"]/h1/text())').get()
        workday = extract(fields, 'Disponibilidad requerida <strong>', '</strong>')
        if workday != 'VACIO':
            it['workday'] = workday
        roles = extract(fields, 'Roles necesarios <strong>', '</strong>')
        if roles != 'VACIO':
            it['roles'] = roles
        it['salary'] = response.xpath('normalize-space(//h4[@class="budget text-success text-right"]/text())').get()
        
        it['description'] = response.xpath('//div[@class="expander js-expander-passed"]/text()[1]').get()
        
        it['requirements'] = " ".join(response.xpath('normalize-space(//p[@class="skills"])').getall())
        it['company_name'] = response.xpath('normalize-space(//*[@id="app"]/div/div[2]/section/section[1]/div/aside/article[3]/div[1]/a/span/text())').get()
        yield it