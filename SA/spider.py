import pymongo
from SA.Spiders.ZhihuSpider2.ZhihuSpider import ZhihuSpider
from scrapy import Item, Field
import datetime

def cmp_datetime(a, b):
    a_datetime = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M')
    b_datetime = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M')

    if a_datetime > b_datetime:
        return -1
    elif a_datetime < b_datetime:
        return 1
    else:
        return 0

def get_weibo_profile(weibo_id):
    '''
    功能 : 根据用户名 和 用户主页地址 返回用户基本信息

    flag : 0 表示成功获取到用户基本信息
           1 表示该用户不存在 或 url不存在
    img : 用户头像
    lcoation : 用户位置
    profile : 用户简介
    '''

    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Sina"]
    Information = db['Information']
    item = Information.find_one({'_id': weibo_id})
    if item:
        return dict(item)
    else:
        return {}

def get_weibo_state(weibo_id):
    '''
    功能 ： 根据用户名 返回 爬取到的该用户的动态（动态内容、发布时间等）

    :param username:
    :return:
    '''

    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Sina"]
    Tweets = db['Tweets']
    item = Tweets.find({'ID': weibo_id})
    if item:
        return  [dict(x) for x in item]
    else:
        return []

def get_zhihu_profile(zhihu_id):
    s = ZhihuSpider()
    document = s.findPerson(zhihu_id)

    return  document

def get_zhihu_state(zhihu_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Tweets = db['Tweets']
    item = Tweets.find({'user': zhihu_id})
    if item:
        return  [dict(x) for x in item]
    else:
        return []

def update_weibo(weibo_id):
    '''

    :param weibo_id:
    :return: int 表示更新出了几条新动态
    '''
    pass

def update_zhihu(zhihu_id):
    '''

    :param zhihu_id:
    :return: int 表示更新出了几条新动态
    '''
    pass

def update_tieba(tieba_id):
    '''

    :param tieba_id:
    :return: int 标识更新出了几条新动态
    '''
    pass

if __name__ == "__main__":
    try:
        print(get_weibo_profile('5066999620'))
        print(get_weibo_state('5066999620'))
    except Exception as e:
        print(e)
