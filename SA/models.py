from django.db import models
from django.contrib.auth.models import User
import os

class Weibo(models.Model):
    username = models.CharField(max_length=100)
    homepage_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200,default=" ")
    location = models.CharField(max_length=100,default=" ")
    profile = models.CharField(max_length=200,default=" ")

    def __str__(self):
        return self.username

class Tieba(models.Model):
    username = models.CharField(max_length=100)
    homepage_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200,default=" ")

    def __str__(self):
        return self.username

class Zhihu(models.Model):
    username = models.CharField(max_length=100)
    homepage_url = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200,default=" ")
    profile = models.CharField(max_length=200,default=" ")

    def __str__(self):
        return self.username

class UserInfo(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=BASE_DIR+'/media/head')
    choice_index = (('F', '女'), ('M', '男'))
    sex = models.CharField(max_length=10, default="M", choices=choice_index)
    weibo_friend = models.ManyToManyField(Weibo)
    tieba_friend = models.ManyToManyField(Tieba)
    zhihu_friend = models.ManyToManyField(Zhihu)

    def __str__(self):
        return self.user.username