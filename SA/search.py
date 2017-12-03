import pymongo

def search_weibo(str):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Sina"]
    Tweets = db['Tweets']
    strings = str.split(' ')
    st = [1] * len(strings)
    for i in range(0, len(strings)):
        st[i] = {'Content': {"$regex": strings[i]}}
    item = Tweets.find(
        {"$and": st}
    ).limit(100)
    if item:
        return [dict(x) for x in item]
    else:
        return []

def search_zhihu(str):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Zhihu"]
    Tweets = db['Tweets']
    strings = str.split(' ')
    st = [1] * len(strings)
    for i in range(0,len(strings)):
        st[i] = {"$or":[
                {'question_title': {"$regex": strings[i]}},
                {'answer_content': {"$regex": strings[i]}}
            ]}
    item = Tweets.find(
        {"$and":st}
    ).limit(100)
    if item:
        return [dict(x) for x in item]
    else:
        return []

def search_tieba(str):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn["Tieba"]
    Tweets = db['Tweets']
    strings = str.split(' ')
    st = [1] * len(strings)
    for i in range(0, len(strings)):
        st[i] = {"$or": [
            {'Content': {"$regex": strings[i]}},
            {'Title': {"$regex": strings[i]}}
        ]}
    item = Tweets.find(
        {"$and": st}
    ).limit(100)
    if item:
        return [dict(x) for x in item]
    else:
        return []

if __name__ == "__main__":
    try:
        a = search_tieba('一米五 世界')
        print(a)
    except Exception as e:
        print(e)