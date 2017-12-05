from bosonnlp import BosonNLP
import pymongo
import datetime
from .spider import  *

nlp = BosonNLP('wsyCNqRz.21248.UXNUZt2FXUBg')

def emotion(weibo_id,zhihu_id,tieba_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Sina"]
    Tweets = db['Tweets']
    weibo_item = Tweets.find({'ID': weibo_id})

    now_time = datetime.datetime.now()
    base_time = str(now_time + datetime.timedelta(days=-30))

    if weibo_item:
        weibo_item = [dict(x) for x in weibo_item]
    else:
        weibo_item = []

    weibo_item2 = []
    for x in weibo_item:
        if 'PubTime' in x.keys():
            if x['PubTime'] > base_time:
                weibo_item2.append(x)

    weibo_item2 = sorted(weibo_item2,key=lambda x:x['PubTime'],reverse=True)

    db = conn["Zhihu"]
    Tweets = db['Tweets']
    zhihu_item = Tweets.find({'user': zhihu_id})

    if zhihu_item:
        zhihu_item = [dict(x) for x in zhihu_item]
    else:
        zhihu_item = []

    zhihu_item2 = []
    for x in zhihu_item:
        if 'created_time' in x.keys():
            if x['created_time'] > base_time:
                zhihu_item2.append(x)

    zhihu_item2 = sorted(zhihu_item2,key=lambda x:x['created_time'],reverse=True)

    db = conn["Tieba"]
    Tweets = db['Tweets']
    tieba_item = Tweets.find({'User': tieba_id})

    if tieba_item:
        tieba_item = [dict(x) for x in tieba_item]
    else:
        tieba_item = []

    tieba_item2 = []
    for x in tieba_item:
        if 'Date' in x.keys():
            if x['Date'] > base_time:
                tieba_item2.append(x)

    tieba_item2 = sorted(tieba_item2,key=lambda x:x['Date'],reverse=True)

    return weibo_item2,zhihu_item2,tieba_item2

def interest(weibo_id,zhihu_id,tieba_id):
    pass

def statistics(weibo_id,zhihu_id,tieba_id):
    recent_3 = datetime.datetime.now()
    recent_3 = str(recent_3 + datetime.timedelta(days=-2))

    recent_7 = datetime.datetime.now()
    recent_7 = str(recent_7 + datetime.timedelta(days=-6))

    recent_30 = datetime.datetime.now()
    recent_30 = str(recent_30 + datetime.timedelta(days=-30))
    has_weibo = False
    has_zhihu = False
    has_tieba = False
    weibo_info = get_weibo_profile(weibo_id)
    weibo_num = {}
    if weibo_info != {}:
        has_weibo = True
        weibo_Tweets = get_weibo_state(weibo_id)
        weibo_num['total'] = weibo_info['Num_Tweets']
        weibo_num['recent_3'] = 0
        weibo_num['recent_7'] = 0
        weibo_num['recent_30'] = 0

        for w in weibo_Tweets:
            if w['PubTime'] > recent_3:
                weibo_num['recent_3'] += 1
                weibo_num['recent_7'] += 1
                weibo_num['recent_30'] += 1
            elif w['PubTime'] > recent_7:
                weibo_num['recent_7'] += 1
                weibo_num['recent_30'] += 1
            elif w['PubTime'] > recent_30:
                weibo_num['recent_30'] += 1
            else:
                break

    zhihu_info = get_zhihu_profile(zhihu_id)
    zhihu_num = {}
    if zhihu_info != {}:
        has_zhihu = True
        zhihu_Tweets = get_zhihu_state(zhihu_id)
        zhihu_num['total'] = zhihu_info['answer_count']
        zhihu_num['recent_3'] = 0
        zhihu_num['recent_7'] = 0
        zhihu_num['recent_30'] = 0

        for w in zhihu_Tweets:
            if w['type'] == 'CREATE_ANSWER':
                if w['created_time'] > recent_3:
                    zhihu_num['recent_3'] += 1
                    zhihu_num['recent_7'] += 1
                    zhihu_num['recent_30'] += 1
                elif w['created_time'] > recent_7:
                    zhihu_num['recent_7'] += 1
                    zhihu_num['recent_30'] += 1
                elif w['created_time'] > recent_30:
                    zhihu_num['recent_30'] += 1
                else:
                    break

    tieba_info = get_tieba_profile(tieba_id)
    tieba_num = {}
    if tieba_info != {}:
        has_tieba = True
        tieba_Tweets = get_tieba_state(tieba_id)
        tieba_num['total'] = tieba_info['Pages'][4:]
        tieba_num['recent_3'] = 0
        tieba_num['recent_7'] = 0
        tieba_num['recent_30'] = 0

        for w in tieba_Tweets:
            if w['Date'] > recent_3:
                tieba_num['recent_3'] += 1
                tieba_num['recent_7'] += 1
                tieba_num['recent_30'] += 1
            elif w['Date'] > recent_7:
                tieba_num['recent_7'] += 1
                tieba_num['recent_30'] += 1
            elif w['Date'] > recent_30:
                tieba_num['recent_30'] += 1
            else:
                break
    return weibo_num,zhihu_num,tieba_num,has_weibo,has_zhihu,has_tieba

if __name__ == '__main__':
    weibo_item,zhihu_item,tieba_item = emotion('5066999620','excited-vczh','你就是陈斯冷')
    for x in weibo_item:
        print(x['PubTime'])
    print('='*20)
    for x in zhihu_item:
        print(x['created_time'])
    print('='*20)
    for x in tieba_item:
        print(x['Date'])

