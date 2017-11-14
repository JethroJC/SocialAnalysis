from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect
from .spider import *

@csrf_exempt
def index(request):
    return render(request, 'SA/index.html')

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        try:
            User.objects.get(username=username)
        except Exception:
            result = {'status': 'error', 'error_message': 'user_not_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            try:
                info['remember_me']
            except Exception:
                request.session.set_expiry(0)
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        result = {'status': 'error', 'error_message': 'wrong_password'}

        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
def user_register(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        try:
            User.objects.get(username=username)
        except Exception:
            password = info['password']
            email = info['email']
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except Exception:
                result = {'status': 'error', 'error_message': 'other'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                UserInfo(user=user).save()
                result = {'status': 'success'}
                return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'error', 'error_message': 'user_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')

@csrf_exempt
@login_required
def home(request):
    return render(request,'SA/home.html',{})

@csrf_exempt
@login_required
def person_info(request):
    user = request.user
    userinfo = user.userinfo

    context = {}
    context['name'] = user.username
    context['email'] = user.email

    if userinfo.sex == 'F':
        context['sex'] = '女'
    else:
        context['sex'] = '男'

    img_path =  userinfo.image.name

    if img_path != '':
            index = img_path.find('/media')
            img_path = img_path[index:]

    context['img_path'] = img_path

    follows = userinfo.follow_set.all()

    context['follows'] = follows

    return render(request,'SA/person_info.html',context)

@csrf_exempt
@login_required
def person_detail(request,follow_id):
    user = request.user
    userinfo = user.userinfo
    friend = Follow.objects.get(id=follow_id)

    context = {}

    follows = userinfo.follow_set.all()
    context['follows'] = follows
    context['follow_id'] = follow_id

    document = get_weibo_profile(friend.weibo_id)
    context['weibo_name'] = document['NickName']
    context['weibo_img_src'] = document['Avator']
    context['weibo_province'] = document['Province']
    context['weibo_city'] = document['City']
    context['weibo_url'] = document['URL']

    context['zhihu_name'] = friend.zhihu_username
    context['friend'] = friend

    context['tieba_name'] = friend.tieba_username

    return render(request,'SA/person_detail.html',context)

@csrf_exempt
@login_required
def add_weibo(request):
    if request.method == 'POST':
        info = request.POST
        username = info['username']
        homepage_url = info['homepage_url']
        weibo_id = info['weibo_id']
        document = get_weibo_profile(weibo_id)

        '''
        if document == {}:
            Weibo(username=username,homepage_url=homepage_url,weibo_id=weibo_id).save()
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'error'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        '''
    else:
        return render_to_response('404.html')

@csrf_exempt
@login_required
def add_tieba(request):
    pass

@csrf_exempt
@login_required
def add_zhihu(request):
    pass

@csrf_exempt
@login_required
def state_weibo(request):
    user = request.user
    userinfo = user.userinfo
    weibo_friends = userinfo.weibo_friend.all()
    friends = []

    for f in weibo_friends:
        states = get_weibo_state(f.weibo_id)
        friend_info = get_weibo_profile(f.weibo_id)

        friend = {}
        friend['info'] = friend_info
        friend['time'] = []
        friend['content'] = []
        friend['like'] = []
        friend['comment_num'] = []

        for state in states:
            friend['time'].append(state['PubTime'])
            friend['content'].append(state['Content'])
            friend['like'].append(state['Like'])
            friend['comment_num'].append(state['Comment'])

        friends.append(friend)

    print(friends)

    return render(request,'SA/state_weibo.html',{})

@csrf_exempt
@login_required
def state_tieba(request):
    return render(request,'SA/state_tieba.html',{})

@csrf_exempt
@login_required
def state_zhihu(request):
    return render(request,'SA/state_zhihu.html',{})

@csrf_exempt
@login_required
def state(request):
    user = request.user
    userinfo = user.userinfo
    weibo_friends = userinfo.weibo_friend.all()
    friends = []

    for f in weibo_friends:
        states = get_weibo_state(f.weibo_id)
        friend_info = get_weibo_profile(f.weibo_id)

        friend = {}
        friend['info'] = friend_info
        friend['time'] = []
        friend['content'] = []
        friend['like'] = []
        friend['comment_num'] = []

        for state in states:
            friend['time'].append(state['PubTime'])
            friend['content'].append(state['Content'])
            friend['like'].append(state['Like'])
            friend['comment_num'].append(state['Comment'])

        friends.append(friend)

    print(friends)

    return render(request,'SA/state_weibo.html',{})




































