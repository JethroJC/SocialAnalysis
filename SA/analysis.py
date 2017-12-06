from bosonnlp import BosonNLP
import pymongo
import datetime
from .spider import  *
from gensim import corpora, models
from scipy.sparse import csr_matrix
import os,re,time,logging
import jieba
import pickle as pkl

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
    weibo_item,zhihu_item,tieba_item = emotion('5066999620','excited-vczh','你就是陈斯冷')
    for x in weibo_item:
        print(x['PubTime'])
    print('='*20)
    for x in zhihu_item:
        print(x['created_time'])
    print('='*20)
    for x in tieba_item:
        print(x['Date'])

