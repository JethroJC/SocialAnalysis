from zhihu_oauth import ZhihuClient, ActType
import pymongo
import  time
class ZhihuSpider:

    client = ZhihuClient()
    client.load_token('./token.pkl')

    def updateAll(self):
        db_client = pymongo.MongoClient("localhost", 27017)
        db = db_client["Zhihu"]
        Information = db["Information"]
        for p in Information.find({}, {'_id':1}):
            print('Updating ', p['_id'])
            self.updatePerson(p['_id'])

        db_client.close()

    def updatePerson(self, name):
        try:
            p = self.client.people(name)
            db_client = pymongo.MongoClient("localhost", 27017)
            db = db_client["Zhihu"]
            Tweets = db["Tweets"]
            k = 0
            for act in p.activities:
                if act.type == ActType.COLLECT_ANSWER:
                    answer = act.target.answer
                    question = answer.question
                    collection = act.target.collection

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'COLLECT_ANSWER'

                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['question_id'] = question.id
                    d['question_title'] = question.title

                    d['answer_id'] = answer.id
                    d['answer_content'] = answer.content

                    d['collection_id'] = collection.id
                    d['collection_title'] = collection.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.COLLECT_ARTICLE:
                    article = act.target.article
                    collection = act.target.collection

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'COLLECT_ARTICLE'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['article_id'] = article.id
                    d['article_title'] = article.title
                    d['article_content'] = article.content

                    d['collection_id'] = collection.id
                    d['collection_title'] = collection.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type==ActType.CREATE_ANSWER:
                    answer = act.target
                    question = answer.question

                    d = {'_id': name+str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'CREATE_ANSWER'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['question_id'] = question.id
                    d['question_title'] = question.title

                    d['answer_id'] = answer.id
                    d['answer_content'] = answer.content

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k+1
                    if k==100:
                        break

                elif act.type==ActType.CREATE_ARTICLE:
                    article = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'CREATE_ARTICLE'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['article_id'] = article.id
                    d['article_title'] = article.title
                    d['article_content'] = article.content

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k+1
                    if k==100:
                        break

                elif act.type==ActType.CREATE_QUESTION:
                    question = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'CREATE_QUESTION'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['question_id'] = question.id
                    d['question_title'] = question.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.FOLLOW_COLLECTION:
                    collection = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'FOLLOW_COLLECTION'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['collection_id'] = collection.id
                    d['collection_title'] = collection.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.FOLLOW_COLUMN:
                    column = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'FOLLOW_COLUMN'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['column_id'] = column.id
                    d['column_description'] = column.description
                    d['column_title'] = column.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type==ActType.FOLLOW_QUESTION:
                    question = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'FOLLOW_QUESTION'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['question_id'] = question.id
                    d['question_title'] = question.title

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.FOLLOW_TOPIC:
                    topic = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'FOLLOW_TOPIC'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['topic_id'] = topic.id
                    d['topic_name'] = topic.name
                    d['topic_avatar_url'] = topic.avatar_url

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.VOTEUP_ANSWER:
                    answer = act.target
                    question = answer.question

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'VOTEUP_ANSWER'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)


                    d['question_id'] = question.id
                    d['question_title'] = question.title

                    d['answer_id'] = answer.id
                    d['answer_content'] = answer.content

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

                elif act.type == ActType.VOTEUP_ARTICLE:
                    article = act.target

                    d = {'_id': name + str(act.created_time)}
                    d['user'] = name
                    d['type'] = 'VOTEUP_ARTICLE'
                    timestamp = act.created_time
                    time_local = time.localtime(timestamp)
                    d['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

                    d['article_id'] = article.id
                    d['article_title'] = article.title
                    d['article_content'] = article.content

                    if Tweets.find({'_id': d['_id']}).count() > 0:
                        Tweets.update({'_id': d['_id']}, {'$set': d})
                        break
                    else:
                        Tweets.insert(d)

                    k = k + 1
                    if k == 100:
                        break

            db_client.close()
        except Exception as e:
            print('error:', e)

    def findPerson(self,name):
        try:
            p = self.client.people(name)
            print('name', p.name)
            d = {'_id': name, 'name': p.name}
            d['answer_count'] = p.answer_count
            d['article_count'] = p.article_count
            d['articles_count'] = p.articles_count
            d['avatar_url'] = p.avatar_url
            return d
        except Exception as e:
            print('Error',e)
            return {}

    def addPerson(self,name):
        try:
            p = self.client.people(name)
            d = {'_id': name, 'name': p.name}
            d['answer_count'] = p.answer_count
            d['article_count'] = p.article_count
            d['articles_count'] = p.articles_count
            d['avatar_url'] = p.avatar_url
            db_client = pymongo.MongoClient("localhost", 27017)
            db = db_client["Zhihu"]
            Information = db["Information"]
            if Information.find({'_id': d['_id']}).count() > 0:
                Information.update({'_id': d['_id']}, {'$set': d})
            else:
                Information.insert(d)
            db_client.close()
            self.updatePerson(name)
            return d
        except Exception as e:
            print('Error',e)
            return {}

if __name__ == "__main__":
    s = ZhihuSpider()
    s.updateAll()
    #s.addPerson('qian-ni-ma-82')

    # s.updateAll()