from django.shortcuts import render
from .models import UserInfo
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

    return render(request,'SA/person_info.html',context)

@csrf_exempt
def person_weibo(request):
    return render(request,'SA/person_weibo.html',{})

@csrf_exempt
def add_weibo(request):
    if request.method == 'POST':
        info = request.POST
        username = info['username']
        homepage_url = info['homepage_url']
        flag,img,location,profile = get_weibo_profile(username,homepage_url)

        if flag == 0:
            pass
        else:
            pass
    else:
        return render_to_response('404.html')

@csrf_exempt
def person_tieba(request):
    return render(request,'SA/person_tieba.html',{})

@csrf_exempt
def person_zhihu(request):
    return render(request,'SA/person_zhihu.html',{})

@csrf_exempt
def state_weibo(request):
    return render(request,'SA/state_weibo.html',{})

@csrf_exempt
def state_tieba(request):
    return render(request,'SA/state_tieba.html',{})

@csrf_exempt
def state_zhihu(request):
    return render(request,'SA/state_zhihu.html',{})




































