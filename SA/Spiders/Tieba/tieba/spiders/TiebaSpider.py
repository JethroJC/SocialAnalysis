import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

from tieba.items import TweetItem
from tieba.config import tiebaID

class TiebaSpider(scrapy.Spider):
    name = "Tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = list(set(tiebaID))

    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="http://tieba.baidu.com/home/main?un=%s" % uid, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//div[@class="n_right clearfix"]')
        for div in divs:
            tweetItem = TweetItem()
            date = div.xpath('div[@class="n_post_time"]//text()').extract()
            if len(div.xpath('div[@class="n_type type_zhuti"]')) > 0:
                tweetItem['Type'] = 'zhuti'
                tieba_name = div.xpath('div/div/div[@class="thread_name"]/a[@class="n_name"]//text()').extract()
                tieba_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="n_name"]/@href').extract()
                title = div.xpath('div/div/div[@class="thread_name"]/a[@class="title"]//text()').extract()
                title_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="title"]/@href').extract()
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
                tieba_name = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="n_name"]//text()').extract()
                tieba_url = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="n_name"]/@href').extract()
                title = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="titletxt"]//text()').extract()
                title_url = div.xpath('div/div[@class="n_txt_huifu"]/a[@class="titletxt"]/@href').extract()
                content = div.xpath('div/div/div[@class="thread_name"]/a[@class="reply_content"]//text()').extract()
                content_url = div.xpath('div/div/div[@class="thread_name"]/a[@class="reply_content"]/@href').extract()
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
