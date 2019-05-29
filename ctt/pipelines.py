# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo


class CttPipeline(object):

    def __init__(self):
        self.file = open('./Ctt_items.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if item['name']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        return item

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("127.0.0.1", 27017, connect=True)
        self.db = self.client['Ctt']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.db["ctt"].update({'company_name': item['company_name']}, dict(item), True):
            print()
        else:
            print("No Mongodb")
        return item

