from django.db import models
from django.contrib.auth.models import User
import os

class UserInfo(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=BASE_DIR+'/media/head')
    choice_index = (('F', '女'), ('M', '男'))
    sex = models.CharField(max_length=10, default="M", choices=choice_index)
