import scrapy


class XcwSpider(scrapy.Spider):
    name = 'xcw'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://ctrip.com/re']

    def parse(self, response):
        pass
