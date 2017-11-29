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

    if 'Province' in document:
        context['weibo_province'] = document['Province']

    if 'City' in document:
        context['weibo_city'] = document['City']

    context['weibo_url'] = document['URL']
    context['friend'] = friend

    context['zhihu_name'] = friend.zhihu_username
    if not friend.zhihu_username == '':
        document2 = get_zhihu_profile(friend.zhihu_id)

        context['zhihu_img_src'] = document2['avatar_url']
        context['answer_count'] = document2['answer_count']
        context['articles_count'] = document2['articles_count']

    context['tieba_name'] = friend.tieba_username

    return render(request,'SA/person_detail.html',context)

@csrf_exempt
@login_required
def add_weibo(request):
    if request.method == 'POST':
        try:
            info = request.POST
            username = info['username']
            homepage_url = info['homepage_url']
            weibo_id = info['weibo_id']
            follow_id = info['follow_id']

            follow = Follow.objects.get(id=follow_id)
            follow.weibo_id = weibo_id
            follow.weibo_url = homepage_url

            result = {'status':'success'}

            return HttpResponse(json.dumps(result), content_type='application/json')
        except :
            result = {'status':'error'}

            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')

@csrf_exempt
@login_required
def add_tieba(request):
    pass

@csrf_exempt
@login_required
def add_zhihu(request):
    if request.method == 'POST':
        try:
            info = request.POST
            username = info['username']
            homepage_url = info['homepage_url']
            follow_id = info['follow_id']

            follow = Follow.objects.get(id=follow_id)
            follow.zhihu_username =username
            follow.zhihu_url = homepage_url
            follow.zhihu_id = homepage_url.split('/')[4]
            follow.save()

            result = {'status':'success'}

            return HttpResponse(json.dumps(result), content_type='application/json')
        except :
            result = {'status':'error'}

            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')

@csrf_exempt
@login_required
def state(request):
    user = request.user
    userinfo = user.userinfo

    follows = userinfo.follow_set.all()

    context = {}
    context['follows'] = follows

    return render(request,'SA/state.html',context)

@csrf_exempt
@login_required
def state_detail(request,follow_id):
    user = request.user
    userinfo = user.userinfo
    friend = Follow.objects.get(id=follow_id)
    follows = userinfo.follow_set.all()

    context = {}

    context['follows'] = follows

    weibo_profile = get_weibo_profile(friend.weibo_id)
    context['weibo_img_src'] = weibo_profile['Avator']
    context['weibo_url'] = weibo_profile['URL']
    context['weibo_name'] = weibo_profile['NickName']

    weibo_states = get_weibo_state(friend.weibo_id)
    context['weibo'] = []

    for s in weibo_states:
        temp = {}
        temp['weibo_content'] = s['Content']
        if 'PubTime' in s:
            temp['weibo_time'] = s['PubTime']
        temp['weibo_comment'] = s['Comment']

        context['weibo'].append(temp)

    return render(request,'SA/state_detail.html',context)








































