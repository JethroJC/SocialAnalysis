#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline
import sys
if len(sys.argv) == 1:
    cmdline.execute("scrapy crawl Tieba".split(" "))
else:
    cmdline.execute(("scrapy crawl Tieba -a category=%s" % sys.argv[1]).split(" "))