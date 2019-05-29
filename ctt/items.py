# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CttItem1(scrapy.Item):
    # define the fields for your item here like:
    name1 = scrapy.Field()
    name2 = scrapy.Field()
    link = scrapy.Field()
    fk = scrapy.Field()
    nicename_id = scrapy.Field()
    tel = scrapy.Field()
    address = scrapy.Field()
    Settled_rate = scrapy.Field()
    Total = scrapy.Field()
    explain = scrapy.Field()
    Fraction = scrapy.Field()
    g_q_f = scrapy.Field()
    wz = scrapy.Field()
    Site = scrapy.Field()
    rs = scrapy.Field()
    S = scrapy.Field()
    parse_link = scrapy.Field()

class CttItem(scrapy.Item):
    parse_link = scrapy.Field()
    nicename_id = scrapy.Field()
    tel = scrapy.Field()
    company_name = scrapy.Field()
    info = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    address = scrapy.Field()
    city_name = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
