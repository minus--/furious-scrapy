# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    code = scrapy.Field()
    price = scrapy.Field()
    dci = scrapy.Field()
    lab = scrapy.Field()
    med_class = scrapy.Field()
    disp_part = scrapy.Field()

