from django.db import models
from django.contrib.auth.models import User
import os

class UserInfo(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=BASE_DIR+'/media/head')
    choice_index = (('F', '女'), ('M', '男'))
    sex = models.CharField(max_length=10, default="M", choices=choice_index)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    '''
    微博通过微博id查询
    知乎通过知乎id查询,知乎id通过url截取得到
    '''
    tag_name = models.CharField(max_length=100,default=" ",blank=True)
    weibo_url = models.CharField(max_length=200,default=" ",blank=True)
    weibo_id = models.CharField(max_length=20,default=" ",blank=True)
    tieba_username = models.CharField(max_length=100,default=" ",blank=True)
    tieba_url = models.CharField(max_length=200,default=" ",blank=True)
    zhihu_username = models.CharField(max_length=100,default=" ",blank=True)
    zhihu_url = models.CharField(max_length=200,default=" ",blank=True)
    zhihu_id = models.CharField(max_length=20,default=" ",blank=True)

    follow_by = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.tag_name