# encoding: utf-8
import re

text = open('input.html', encoding='UTF-8')
a = text.read()
ans = re.findall('<div class="c">.*"(.*?)" alt="头像">', a)
print(len(ans))
print(ans)