from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
import json
import time
import operator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, \
    HttpResponse, HttpResponseRedirect
from .spider import *
from django.utils.safestring import mark_safe


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

    weibo_flag = False
    zhihu_flag = False
    tieba_flag = False

    #微博
    if not friend.weibo_url == '':
        weibo_flag = True
        document = get_weibo_profile(friend.weibo_id)
        context['weibo_name'] = document['NickName']
        context['weibo_img_src'] = document['Avator']

        if 'Province' in document:
            context['weibo_province'] = document['Province']

        if 'City' in document:
            context['weibo_city'] = document['City']

        context['weibo_url'] = document['URL']
        context['friend'] = friend

    #知乎
    if not friend.zhihu_url == '':
        zhihu_flag = True
        document2 = get_zhihu_profile(friend.zhihu_id)
        print(document2)
        context['zhihu_name'] = document2['name']
        context['zhihu_img_src'] = document2['avatar_url']
        context['answer_count'] = document2['answer_count']
        context['articles_count'] = document2['articles_count']

    #贴吧
    if not friend.tieba_username == '':
        tieba_flag = True
        document3 = get_tieba_profile(friend.tieba_username)
        context['tieba_name'] = document3['Name']
        context['tieba_age'] = document3['Age']
        context['tieba_pages'] = document3['Pages'][4:]
        context['tieba_follow'] = document3['Follows'].split(' ')


    context['weibo_flag'] = weibo_flag
    context['zhihu_flag'] = zhihu_flag
    context['tieba_flag'] = tieba_flag

    return render(request,'SA/person_detail.html',context)


@csrf_exempt
@login_required
def add_person(request):
    if request.method == 'POST':
        try:
            info = request.POST
            user = request.user
            userinfo = user.userinfo
            new_follow  = Follow(follow_by=userinfo)

            new_follow.tag_name = info['username']
            new_follow.weibo_id = info['weibo_id']
            new_follow.weibo_url = info['weibo_homepage_url']
            new_follow.zhihu_url = info['zhihu_homepage_url']
            homepage_url = info['zhihu_homepage_url']
            index1 = homepage_url.find('people')
            homepage_url = homepage_url[index1+7:]
            index2 = homepage_url.find('/')
            new_follow.zhihu_id = homepage_url[:index2]
            new_follow.tieba_username = info['tieba_username']

            new_follow.save()

            result = {'status':'success'}

            return HttpResponse(json.dumps(result), content_type='application/json')
        except :
            result = {'status':'error'}

            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
@login_required
def add_weibo(request):
    if request.method == 'POST':
        try:
            info = request.POST
            homepage_url = info['homepage_url']
            weibo_id = info['weibo_id']
            follow_id = info['follow_id']

            follow = Follow.objects.get(id=follow_id)
            follow.weibo_id = weibo_id
            follow.weibo_url = homepage_url
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
def add_tieba(request):
    if request.method == 'POST':
        try:
            info = request.POST
            username = info['username']
            follow_id = info['follow_id']
            follow = Follow.objects.get(id=follow_id)
            follow.tieba_username = username
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
def add_zhihu(request):
    if request.method == 'POST':
        try:
            info = request.POST
            homepage_url = info['homepage_url']
            follow_id = info['follow_id']

            follow = Follow.objects.get(id=follow_id)
            follow.zhihu_url = homepage_url
            index1 = homepage_url.find('people')
            homepage_url = homepage_url[index1+7:]
            index2 = homepage_url.find('/')
            follow.zhihu_id = homepage_url[:index2]
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
    context['follow_id'] = follow_id

    #微博动态
    weibo_profile = get_weibo_profile(friend.weibo_id)
    context['weibo_img_src'] = weibo_profile['Avator']
    context['weibo_url'] = weibo_profile['URL']
    context['weibo_name'] = weibo_profile['NickName']

    weibo_states = get_weibo_state(friend.weibo_id)
    #weibo_states = weibo_states.sort(key=lambda x:datetime.datetime.strptime(x['PubTime'],'%Y-%m-%d %H:%M') if 'PubTime' in x else datetime.datetime())
    context['weibo'] = []

    for s in weibo_states:
        temp = {}
        temp['weibo_content'] = s['Content']
        if 'PubTime' in s:
            temp['weibo_time'] = s['PubTime']
        temp['weibo_comment'] = s['Comment']

        context['weibo'].append(temp)

    #知乎动态
    zhihu_states = get_zhihu_state(friend.zhihu_id)
    for s in zhihu_states:
        timestamp = s['created_time']
        time_local = time.localtime(timestamp)
        s['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        if s['type'] == 'VOTEUP_ANSWER':
            s['answer_content'] = mark_safe(s['answer_content'])
        elif s['type'] == 'CREATE_ANSWER':
            s['answer_content'] = mark_safe(s['answer_content'])
        else:
            pass

    context['zhihu'] = zhihu_states

    #贴吧动态
    tieba_states = get_tieba_state(friend.tieba_username)
    context['tieba'] = tieba_states
    return render(request,'SA/state_detail.html',context)

@csrf_exempt
@login_required
def update_weibo1(request,follow_id):
    follow = Follow.objects.get(id=follow_id)
    num = update_weibo(follow.weibo_id)
    print(num)
    result = {'status':'success'}

    return HttpResponse(json.dumps(result), content_type='application/json')







































