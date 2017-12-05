import pymongo
from SA.Spiders.ZhihuSpider2.ZhihuSpider import ZhihuSpider
import os
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
        item = [dict(x) for x in item]

        weibo_item2 = []
        for x in item:
            if 'PubTime' in x.keys():
                weibo_item2.append(x)
        weibo_item2 = sorted(weibo_item2,key=lambda x:x['PubTime'],reverse=True)
        return  weibo_item2
    else:
        return []

def get_zhihu_profile(zhihu_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Information = db['Information']
    item = Information.find_one({'_id': zhihu_id})
    if item:
        return dict(item)
    else:
        return {}

    #s = ZhihuSpider()
    #document = s.findPerson(zhihu_id)

def get_zhihu_state(zhihu_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Tweets = db['Tweets']
    item = Tweets.find({'user': zhihu_id})
    if item:
        return  [dict(x) for x in item]
    else:
        return []

def get_tieba_profile(Tieba_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Tieba"]
    Information = db['Information']
    item = Information.find_one({'_id': Tieba_id})
    if item:
        return dict(item)
    else:
        return {}

    #s = ZhihuSpider()
    #document = s.findPerson(zhihu_id)

def get_tieba_state(Tieba_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Tieba"]
    Tweets = db['Tweets']
    item = Tweets.find({'User': Tieba_id})
    if item:
        return  [dict(x) for x in item]
    else:
        return []

def update_weibo(weibo_id):
    '''

    :param weibo_id:
    :return: int 表示更新出了几条新动态
    '''
    print('haha')
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Weibo"]
    Tweets = db['Tweets']
    count_before = Tweets.find({'ID': weibo_id}).count()
    os.chdir('SA/Spiders/WeiboSpider-master/')
    os.system(('python run.py %s' % weibo_id))
    os.chdir('../../../')
    count_after = Tweets.find({'ID': weibo_id}).count()
    return count_after - count_before

def update_zhihu(zhihu_id):
    '''

    :param zhihu_id:
    :return: int 表示更新出了几条新动态
    '''
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Tweets = db['Tweets']
    count_before = Tweets.find({'user': zhihu_id}).count()
    s = ZhihuSpider()
    s.updatePerson(zhihu_id)
    count_after = Tweets.find({'user': zhihu_id}).count()
    return count_after - count_before

def update_tieba(tieba_id):
    '''

    :param tieba_id:
    :return: int 标识更新出了几条新动态
    '''
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Tieba"]
    Tweets = db['Tweets']
    count_before = Tweets.find({'User': tieba_id}).count()
    os.chdir('SA/Spiders/Tieba/')
    os.system(('python run.py %s' % tieba_id))
    os.chdir('../../../')
    count_after = Tweets.find({'User': tieba_id}).count()
    return count_after - count_before

if __name__ == "__main__":
    try:
        #os.chdir('../')
        print(update_weibo('5066999620'))
    except Exception as e:
        print(e)
