# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XcItem(scrapy.Item):
    # define the fields for your item here like:
    J_id = scrapy.Field()
    J_name = scrapy.Field()
    level = scrapy.Field()
    overallScore = scrapy.Field()
    label = scrapy.Field()
    totalCount = scrapy.Field()
    js = scrapy.Field()
    qw = scrapy.Field()
    xjb = scrapy.Field()
