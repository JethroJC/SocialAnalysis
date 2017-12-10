import pymongo
import os
from gensim import corpora, models
from scipy.sparse import csr_matrix
import jieba
import pickle as pkl

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

def get_zhihu_state(zhihu_id):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Tweets = db['Tweets']
    item = Tweets.find({'user': zhihu_id})
    if item:
        return  [dict(x) for x in item]
    else:
    	return []

def interest(weibo_id,zhihu_id):
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

conn = pymongo.MongoClient("localhost", 27017)
db = conn['Sina']
db['Interest'].remove()
db = conn['Zhihu']
db['Interest'].remove()
for line in open('id_list.txt'):
	ids = line.split('**')
	weibo_id = ids[1]
	zhihu_id = ids[2]

	weibo_interest,zhihu_interest,has_weibo,has_zhihu = interest(weibo_id,zhihu_id)

	if has_weibo:
	    db = conn["Sina"]
	    Interest = db['Interest']
	    Interest.insert({'id':weibo_id,'weibo_interest':weibo_interest})
	if has_zhihu:
		db = conn["Zhihu"]
		Interest = db['Interest']
		Interest.insert({'id':zhihu_id,'zhihu_interest':zhihu_interest})
























