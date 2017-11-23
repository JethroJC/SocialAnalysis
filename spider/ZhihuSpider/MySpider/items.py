# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InformationItem(Item):
    _id = Field()
    NickName = Field()
    Gender = Field()
    Province = Field()
    City = Field()
    BriefIntroduction = Field()
    Birthday = Field()
    Num_Tweets = Field()
    Num_Follows = Field()
    Num_Fans = Field()
    SexOrientation = Field()
    Sentiment = Field()
    VIPlevel = Field()
    Authentication = Field()
    URL = Field()
    Avator = Field()

class TweetsItem(Item):
    """ ΢����Ϣ """
    _id = Field()
    ID = Field()
    Content = Field()
    PubTime = Field()
    Co_oridinates = Field()
    Tools = Field()
    Like = Field()
    Comment = Field()
    Transfer = Field()
