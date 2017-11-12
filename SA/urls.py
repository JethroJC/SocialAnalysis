from .views import *
from django.conf.urls import url,include

person_pattern = [
    url(r'^$',person_info,name='person_info'),
    url(r'^person_weibo/$',person_weibo,name='person_weibo'),
    url(r'^person_tieba/$',person_tieba,name='person_tieba'),
    url(r'^person_zhihu/$',person_zhihu,name='person_zhihu'),
    url(r'^add_weibo/$',add_weibo,name='add_weibo'),
    url(r'^add_tieba/$',add_tieba,name='add_tieba'),
    url(r'^add_zhihu/$',add_zhihu,name='add_zhihu'),
]

state_pattern = [
    url(r'^$',state_weibo,name='state_weibo'),
    url(r'^state_tieba/$',state_tieba,name='state_tieba'),
    url(r'^state_zhihu/$',state_zhihu,name='state_zhihu'),
]

analysis_pattern = [

]

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^user_login$', user_login, name='user_login'),
    url(r'^user_register$', user_register, name='user_register'),
    url(r'^home/$',home,name='home'),
    url(r'^person/',include(person_pattern)),
    url(r'^state/',include(state_pattern)),
    url(r'^analysis/',include(analysis_pattern)),
]