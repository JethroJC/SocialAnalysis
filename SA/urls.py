from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^user_login$', user_login, name='user_login'),
    url(r'^user_register$', user_register, name='user_register'),
    url(r'^home/$',home,name='home'),
]