# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from sina.items import RelationshipsItem, TweetsItem, InformationItem


class MongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Relationships = db["Relationships"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, RelationshipsItem):
            try:
                self.Relationships.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                data = dict(item)
                if self.Tweets.find({'_id': data['_id']}).count() > 0:
                    self.Tweets.update({'_id': data['_id']}, {'$set': data})
                else:
                    self.Tweets.insert(dict(item))
            except Exception as e:
                pass
        elif isinstance(item, InformationItem):
            try:
                data = dict(item)
                print('Finding......' + data['_id'])
                if self.Information.find({'_id': data['_id']}).count() > 0:
                    self.Information.update({'_id': data['_id']}, {'$set': data})
                else:
                    self.Information.insert(dict(item))
            except Exception:
                pass
        return item
