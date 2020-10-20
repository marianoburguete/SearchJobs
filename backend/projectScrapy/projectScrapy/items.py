# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CTItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    workday = scrapy.Field()    
    contract_type = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    requirements = scrapy.Field()
    company_name = scrapy.Field()
    company_logo = scrapy.Field()

class WOItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    workday = scrapy.Field()
    contract_type = scrapy.Field()
    roles = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    requirements = scrapy.Field()
    company_name = scrapy.Field()
    
class MTItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    workday = scrapy.Field()    
    contract_type = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    requirements = scrapy.Field()
    company_name = scrapy.Field()
    company_logo = scrapy.Field()
    
