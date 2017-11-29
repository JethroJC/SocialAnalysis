
import re
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

class ZhihuSpider(Spider):
    name = "ZhihuSpider"
    host = "https://www.zhihu.com"
    #start_urls = ["https://weibo.com/u/1678105910?is_all=1",]

    def start_requests(self):
       yield Request(url="https://www.zhihu.com/people/excited-vczh/answers", callback=self.parse_information)

    def parse_information(self, response):
        selector = Selector(response)

        divs = selector.xpath('//div[@class="List-item"]')

        div = divs[1]
        id = div.xpath('@id').extract_first()

