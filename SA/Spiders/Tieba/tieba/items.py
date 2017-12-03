# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TweetItem(scrapy.Item):
    _id = scrapy.Field()
    User = scrapy.Field()
    Type  = scrapy.Field()
    Tieba_name = scrapy.Field()
    Tieba_url = scrapy.Field()
    Title = scrapy.Field()
    Title_url = scrapy.Field()
    Content = scrapy.Field()
    Content_url = scrapy.Field()
    Date = scrapy.Field()

class Information(scrapy.Item):
    _id = scrapy.Field()
    Name = scrapy.Field()
    Age = scrapy.Field()
    Pages = scrapy.Field()
    Follows = scrapy.Field()
