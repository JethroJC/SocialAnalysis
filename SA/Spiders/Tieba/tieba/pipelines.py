# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from tieba.items import TweetItem, Information

class TiebaPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Tieba"]
        self.Tweets = db["Tweets"]
        self.Information = db["Information"]

    def process_item(self, item, spider):
        if isinstance(item, TweetItem):
            try:
                data = dict(item)
                if self.Tweets.find({'_id': data['_id']}).count() > 0:
                    self.Tweets.update({'_id': data['_id']}, {'$set': data})
                else:
                    self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, Information):
            try:
                data = dict(item)
                if self.Information.find({'_id': data['_id']}).count() > 0:
                    self.Information.update({'_id': data['_id']}, {'$set': data})
                else:
                    self.Information.insert(dict(item))
            except Exception:
                pass
        return item
