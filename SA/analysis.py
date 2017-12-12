import pymongo
import datetime
from .spider import  *
import json
import requests

url='http://api.bosonnlp.com/sentiment/analysis?weibo'
headers = {'X-Token':'wsyCNqRz.21248.UXNUZt2FXUBg'}

def emotion(weibo_id):
    weibo_tweets = get_weibo_state(weibo_id)
    now_time = datetime.datetime.now()
    base_time = str(now_time + datetime.timedelta(days=-15))[:10]
    base_time_date = datetime.datetime.strptime(base_time,'%Y-%m-%d')
    index = []
    for i in range(15):
        temp = str(now_time + datetime.timedelta(days=-i))[5:10]
        index.append(temp)

    has_weibo = False
    weibo_emotion = [ []  for i in range(15)]
    if weibo_tweets != []:
        has_weibo = True
        for w in weibo_tweets:
            if w['PubTime'] > base_time:
                weibo_date = datetime.datetime.strptime(w['PubTime'][:10],'%Y-%m-%d')
                gap = int(str(weibo_date - base_time_date)[:2])
                weibo_emotion[gap].append(w['Content'])
            else:
                break

    positive_score = [0 for i in range(15)]
    negative_score = [0 for i in range(15)]

    for i,day in enumerate(weibo_emotion):
        if day == []:
            positive_score[i] = 0
            negative_score[i] = 0
        else:
            data = json.dumps(day)
            res = requests.post(url, headers=headers, data=data.encode('utf-8'))
            scores = json.loads(res.text)

            num = 0

            for score in scores:
                num += 1
                positive_score[i] += float(score[0])*100
                negative_score[i] += float(score[1])*100

            positive_score[i] = positive_score[i]/num
            negative_score[i] = negative_score[i]/num

    return positive_score,negative_score,index

def interest(weibo_id,zhihu_id):
    has_weibo = False
    has_zhihu = False

    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Sina"]
    weibo_interest = db['Interest'].find_one({'id':weibo_id})
    db = conn['Zhihu']
    zhihu_interest = db['Interest'].find_one({'id':zhihu_id})

    if weibo_interest:
        weibo_interest = dict(weibo_interest)
        weibo_interest = weibo_interest['weibo_interest']
        has_weibo = True
    else:
        weibo_interest = []

    if zhihu_interest:
        zhihu_interest = dict(zhihu_interest)
        zhihu_interest = zhihu_interest['zhihu_interest']
        has_zhihu = True
    else:
        zhihu_interest = []

    return weibo_interest,zhihu_interest,has_weibo,has_zhihu


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
    weibo_emotion = emotion('5066999620')
    print(weibo_emotion)


