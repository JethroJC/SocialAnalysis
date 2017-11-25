
import re
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

class ZhihuSpider(Spider):
    name = "Zhihu"
    host = "https://zhihu.com"
    #start_urls = ["https://weibo.com/u/1678105910?is_all=1",]

    def start_requests(self):
       for uid in self.start_urls:
            yield Request(url="https://www.zhihu.com/people/%s/activities" % uid, callback=self.parse_information)

    def parse_information(self, response):
        selector = Selector(response)
        ID = re.findall('(\d+)/profile', response.url)[0]
        divs = selector.xpath('body/div[@class="c" and @id]')