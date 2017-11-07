from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class WeiboSpider(Spider):
    name = "Weibo"
    allowed_domains = ["weibo.com"]
    start_urls = ["https://weibo.com/u/1678105910?is_all=1",]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'YF-Page-G0=e44a6a701dd9c412116754ca0e3c82c3; login_sid_t=930cc9387dead2793af8e1eba5d0aaa0; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; YF-V5-G0=55fccf7be1706b6814a78384fa94e30c; _s_tentry=-; Apache=2249298865818.1235.1510048935573; SINAGLOBAL=2249298865818.1235.1510048935573; ULV=1510048936360:1:1:1:2249298865818.1235.1510048935573:; SSOLoginState=1510049203; SUB=_2A253BfXkDeRhGeNH61YR8C_LyTiIHXVUc2AsrDV8PUNbmtBeLXbCkW-S_02q3RmNIDHF90_qldG_ItKxSQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFR0T-Bh69-XsEVGM_oopzh5JpX5KzhUgL.Fo-4ehB7eh2NeoB2dJLoI7yWqcHkeK.N1Btt; SUHB=0XDl7Lq1M76fUm; ALF=1541585202; httpsupgrade_ab=SSL; wvr=6; TC-V5-G0=7975b0b5ccf92b43930889e90d938495',
                'Host': 'weibo.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            })

    def parse_with_cookie(self, response):
        #filename = response.url.split("/")[-2]
        open('pagewatch.txt', 'wb').write(response.body)
        # sel = HtmlXPathSelector(response)
        # sites = sel.xpath('//div[@class="one-cont-title clearfix"]//i')
        # for site in sites:
        #     content = site.xpath('text()').extract()
        #     print(content)