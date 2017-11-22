from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class ZhihuSpider(Spider):
    name = "Zhihu"
    host = "https://zhihu.com"
    #start_urls = ["https://weibo.com/u/1678105910?is_all=1",]

    def start_requests(self):
       for uid in self.start_urls:
            yield Request(url="https://www.zhihu.com/people/%s/activities" % uid, callback=self.parse_information)

    def parse_information(self, response):
        #filename = response.url.split("/")[-2]
        open('pagewatch.txt', 'wb').write(response.body)
        # sel = HtmlXPathSelector(response)
        # sites = sel.xpath('//div[@class="one-cont-title clearfix"]//i')
        # for site in sites:
        #     content = site.xpath('text()').extract()
        #     print(content)