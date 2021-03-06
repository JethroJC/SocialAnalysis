from .views import *
from django.conf.urls import url,include

person_pattern = [
    url(r'^$',person_info,name='person_info'),
    url(r'^(?P<follow_id>[0-9]+)/$',person_detail,name='person_detail'),
    url(r'^add_weibo/$',add_weibo,name='add_weibo'),
    url(r'^add_tieba/$',add_tieba,name='add_tieba'),
    url(r'^add_zhihu/$',add_zhihu,name='add_zhihu'),
    url(r'^add_person/$',add_person,name='add_person'),
]

state_pattern = [
    url(r'^$',state,name='state'),
    url(r'^(?P<follow_id>[0-9]+)/$',state_detail,name='state_detail'),
    url(r'^update_weibo/(?P<follow_id>[0-9]+)/$',update_weibo1,name='update_weibo'),
]

analysis_pattern = [
    url(r'^statistics_index/$',statistics_index,name='statistics_index'),
    url(r'^statistics/(?P<follow_id>[0-9]+)/$',statistics_detail,name='statistics_detail'),
    url(r'^interest_index/$',interest_index,name='interest_index'),
    url(r'^interest/(?P<follow_id>[0-9]+)/$',interest_detail,name='interest_detail'),
    url(r'^emotion_index/$',emotion_index,name='emotion_index'),
    url(r'^emotion/(?P<follow_id>[0-9]+)/$',emotion_detail,name='emotion_detail'),
    url(r'^get_emotion/(?P<follow_id>[0-9]+)/$',get_emotion,name='get_emotion'),
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