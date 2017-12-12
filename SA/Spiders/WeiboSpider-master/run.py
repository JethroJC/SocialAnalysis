from scrapy import cmdline
import sys
if len(sys.argv) == 1:
    cmdline.execute("scrapy crawl SinaSpider".split(" "))
else:
    cmdline.execute(("scrapy crawl SinaSpider -a category=%s" % sys.argv[1]).split(" "))