# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HackeroneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hid = scrapy.Field()
    reward = scrapy.Field()
    vuln_type = scrapy.Field()
    severity = scrapy.Field()
    submission_date = scrapy.Field()
    resolved_date = scrapy.Field()
    #pass
