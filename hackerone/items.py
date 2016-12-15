# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HackeroneItem(scrapy.Item):
    # Contains the list of fields which will be extracted from bug disclosure report
    hid = scrapy.Field()
    reward = scrapy.Field()
    vuln_type = scrapy.Field()
    severity = scrapy.Field()
    submission_date = scrapy.Field()
    resolved_date = scrapy.Field()