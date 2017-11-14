from .views import *
from django.conf.urls import url,include

person_pattern = [
    url(r'^$',person_info,name='person_info'),
    url(r'^(?P<follow_id>[0-9]+)/$',person_detail,name='person_detail'),
    url(r'^add_weibo/$',add_weibo,name='add_weibo'),
    url(r'^add_tieba/$',add_tieba,name='add_tieba'),
    url(r'^add_zhihu/$',add_zhihu,name='add_zhihu'),
]

state_pattern = [
    url(r'^$',state,name='state'),
    url(r'^(?P<follow_id>[0-9]+)/$',state_detail,name='state_detail'),
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