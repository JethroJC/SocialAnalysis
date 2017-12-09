import pymongo
import datetime
from .spider import  *
from gensim import corpora, models
from scipy.sparse import csr_matrix
import os,re,time,logging
import jieba
import pickle as pkl
import json
import requests

url='http://api.bosonnlp.com/sentiment/analysis?weibo'
headers = {'X-Token':'wsyCNqRz.21248.UXNUZt2FXUBg'}

def emotion(weibo_id):
    pos = [0, 0, 0, 0.21214347805452693, 0.8630134828233795, 0.4348029754653122, 0.9278175281652273, 0.7065262829896948, 0.7392596486152794, 0, 0, 0, 0, 0, 0]
    neg = [0, 0, 0, 0.7878565219454731, 0.13698651717662047, 0.5651970245346878, 0.0721824718347727, 0.29347371701030517, 0.2607403513847207, 0, 0, 0, 0, 0, 0]
    now_time = datetime.datetime.now()
    base_time = str(now_time + datetime.timedelta(days=-15))[:10]
    base_time_date = datetime.datetime.strptime(base_time,'%Y-%m-%d')
    index = []
    for i in range(15):
        temp = str(now_time + datetime.timedelta(days=-i))[5:10]
        index.append(temp)
    i = 0
    for p,n in zip(pos,neg):
        pos[i] = p*100
        neg[i] = n*100
        i += 1

    return pos,neg,index

    '''
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

    return positive_score,negative_score
    '''
def interest(weibo_id,zhihu_id,tieba_id):
    weibo_tweets = get_weibo_state(weibo_id)
    zhihu_tweets = get_zhihu_state(zhihu_id)
    has_weibo = False
    has_zhihu = False
    weibo_interest = {'体育':0, '娱乐':0, '家居':0, '彩票':0, '房产':0, '教育':0, '时尚':0, '时政':0, '星座':0, '游戏':0, '社会':0, '科技':0, '股票':0, '财经':0}
    zhihu_interest = {'体育':0, '娱乐':0, '家居':0, '彩票':0, '房产':0, '教育':0, '时尚':0, '时政':0, '星座':0, '游戏':0, '社会':0, '科技':0, '股票':0, '财经':0}
    if weibo_tweets != []:
        has_weibo = True
        for w in weibo_tweets:
            cat = classify(w['Content'])
            weibo_interest[cat] += 1

    if zhihu_tweets != []:
        has_zhihu = True
        for w in zhihu_tweets:
            if w['type'] == 'CREATE_ANSWER':
                cat = classify(w['answer_content'])
                zhihu_interest[cat] += 1

    weibo_interest = sorted(weibo_interest.items(),key=lambda item:item[1],reverse=True)
    zhihu_interest = sorted(zhihu_interest.items(),key=lambda item:item[1],reverse=True)

    weibo_total = 0.0
    for i,w in enumerate(weibo_interest):
        if w[1] == 0:
            weibo_interest = weibo_interest[:i]
            break
        else:
            weibo_total += w[1]

    zhihu_total = 0.0
    for i,z in enumerate(zhihu_interest):
        if z[1] == 0:
            zhihu_interest = zhihu_interest[:i]
            break
        else:
            zhihu_total += z[1]

    weibo_interest = [(x[0],x[1]/weibo_total*100) for x in weibo_interest]
    zhihu_interest = [(x[0],x[1]/zhihu_total*100) for x in zhihu_interest]

    print(weibo_interest)
    print(zhihu_interest)
    return weibo_interest,zhihu_interest,has_weibo,has_zhihu

def classify(demo_doc):
    path_doc_root = '/Users/jethro/算法设计/TextClassify/THUCNews'
    path_tmp = '/Users/jethro/算法设计/TextClassify/temp'
    path_dictionary     = os.path.join(path_tmp, 'THUNews.dict')
    path_tmp_lsi        = os.path.join(path_tmp, 'lsi_corpus')
    path_tmp_lsimodel   = os.path.join(path_tmp, 'lsi_model.pkl')
    path_tmp_predictor  = os.path.join(path_tmp, 'predictor.pkl')

    dictionary = None
    corpus_tfidf = None
    corpus_lsi = None
    lsi_model = None
    predictor = None

    dictionary = corpora.Dictionary.load(path_dictionary)

    lsi_file = open(path_tmp_lsimodel,'rb')
    lsi_model = pkl.load(lsi_file)
    lsi_file.close()

    x = open(path_tmp_predictor,'rb')
    predictor = pkl.load(x)
    x.close()

    files = os.listdir(path_tmp_lsi)
    catg_list = []

    for file in files:
        temp = file.split('.')[0]
        if temp not in catg_list:
            catg_list.append(temp)

    demo_doc = list(jieba.cut(demo_doc,cut_all=False))
    demo_bow = dictionary.doc2bow(demo_doc)
    tfidf_model = models.TfidfModel(dictionary=dictionary)
    demo_tfidf = tfidf_model[demo_bow]
    demo_lsi = lsi_model[demo_tfidf]

    data = []
    rows = []
    cols = []

    for item in demo_lsi:
        rows.append(0)
        cols.append(item[0])
        data.append(item[1])

    demo_matrix = csr_matrix((data,(rows,cols))).toarray()
    x = predictor.predict(demo_matrix)

    catg = catg_list[x[0]]
    return  catg

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


