from scrapy.spider import Spider

class WeiboSpider(Spider):
    name = "Weibo"
    allowed_domains = ["xiaohua.com"]
    start_urls = ["http://xiaohua.com/",]

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()