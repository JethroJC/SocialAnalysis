# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InformationItem(Item):
    """ ������Ϣ """
    _id = Field()  # �û�ID
    NickName = Field()  # �ǳ�
    Gender = Field()  # �Ա�
    Province = Field()  # ����ʡ
    City = Field()  # ���ڳ���
    BriefIntroduction = Field()  # ���
    Birthday = Field()  # ����
    Num_Tweets = Field()  # ΢����
    Num_Follows = Field()  # ��ע��
    Num_Fans = Field()  # ��˿��
    SexOrientation = Field()  # ��ȡ��
    Sentiment = Field()  # ����״��
    VIPlevel = Field()  # ��Ա�ȼ�
    Authentication = Field()  # ��֤
    URL = Field()  # ��ҳ����
    Avator = Field() #ͷ���ַ

class TweetsItem(Item):
    """ ΢����Ϣ """
    _id = Field()  # �û�ID-΢��ID
    ID = Field()  # �û�ID
    Content = Field()  # ΢������
    PubTime = Field()  # ����ʱ��
    Co_oridinates = Field()  # ��λ����
    Tools = Field()  # ������/ƽ̨
    Like = Field()  # ������
    Comment = Field()  # ������
    Transfer = Field()  # ת����
