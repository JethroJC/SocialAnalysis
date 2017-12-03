#!/usr/bin/env python
# encoding: utf-8

import scrapy
import re
import urllib.parse
from scrapy.selector import Selector
from scrapy.http import Request

from tieba.items import TweetItem, Information
from tieba.config import tiebaID

class TiebaSpider(scrapy.Spider):
    name = "Tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = list(set(tiebaID))

    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="http://tieba.baidu.com/home/main?un=%s" % uid, callback=self.parse)

    def parse(self, response):
        user = re.findall('un=(.*)', response.url)[0]
        selector = Selector(response)
        information = Information()
        name = selector.xpath('//span[@class="userinfo_username "]//text()').extract()
        spans = selector.xpath('//span[@class="user_name"]/span//text()').extract()

        follows = selector.xpath('//div[@id="forum_group_wrap"]/a[not(@title)]/span[not(@class)]//text() |'
                                '//div[@id="forum_group_wrap"]/a[(@title)]/@title').extract()

        information['_id'] = urllib.parse.unquote(user)
        if name:
            information['Name'] = name[0]
        if spans and len(spans) >= 2:
            information['Age'] = spans[0]
            information['Pages'] = spans[1]
        information['Follows'] = " ".join(follows)

        yield information

        divs = selector.xpath('//div[@class="n_right clearfix"]')
        for div in divs:
            tweetItem = TweetItem()
            tweetItem['Date'] = div.xpath('div[@class="n_post_time"]//text()').extract()[0]
            tweetItem['User'] = urllib.parse.unquote(user)
            if len(div.xpath('div[@class="n_type type_zhuti"]')) > 0:
                tweetItem['Type'] = 'zhuti'
                tieba_name = div.xpath('div/div/div[@class="thread_name"]/a[@class="n_name"]//text()').extract()
                tieba_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="n_name"]/@href').extract()
                title = div.xpath('div/div/div[@class="thread_name"]/a[@class="title"]//text()').extract()
                title_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="title"]/@href').extract()
                tweetItem['_id'] = re.findall('pid=(\d+)&', str(title_url))[0]
                if tieba_name:
                    tweetItem['Tieba_name'] = tieba_name[0]
                if tieba_url:
                    tweetItem['Tieba_url'] = tieba_url[0]
                if title:
                    tweetItem['Title'] = title[0]
                if title_url:
                    tweetItem['Title_url'] = title_url[0]
                print(dict(tweetItem))
            elif len(div.xpath('div[@class="n_type type_huifu"]')) > 0:
                tweetItem['Type'] = 'huifu'
                tieba_name = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="n_name"]//text()').extract()
                tieba_url = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="n_name"]/@href').extract()
                title = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="titletxt"]//text()').extract()
                title_url = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="titletxt"]/@href').extract()
                content = div.xpath('div/div/div[@class="thread_name"]/a[@class="reply_content"]//text()').extract()
                content_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="reply_content"]/@href').extract()
                tweetItem['_id'] = re.findall('pid=(\d+)&', str(content_url))[0]
                if tieba_name:
                    tweetItem['Tieba_name'] = tieba_name[0]
                if tieba_url:
                    tweetItem['Tieba_url'] = tieba_url[0]
                if title:
                    tweetItem['Title'] = title[0]
                if title_url:
                    tweetItem['Title_url'] = title_url[0]
                if content:
                    tweetItem['Content'] = content[0]
                if content_url:
                    tweetItem['Content_url'] = content_url[0]
                print(dict(tweetItem))
            yield tweetItem
