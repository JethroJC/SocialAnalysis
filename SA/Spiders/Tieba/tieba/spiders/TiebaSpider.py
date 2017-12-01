import scrapy
from scrapy.selector import Selector

class TiebaSpider(scrapy.Spider):
    name = "Tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/home/main?un=%E4%BA%B2%E4%B8%80%E4%B8%8B%E7%8E%8B%E5%B0%BC%E7%8E%9B",
    ]

    def parse(self, response):
        selector = Selector(response)
        divs = selector.xpath('//div[@class="n_right clearfix"]')
        for div in divs:
            print(div.xpath('div[@class="n_post_time"]//text()').extract())
            print(len(div.xpath('//div[@class="n_type type_zhuti"]')))