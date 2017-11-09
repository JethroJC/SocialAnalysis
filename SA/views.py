from django.shortcuts import render
from .models import UserInfo
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'SA/index.html', {})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        info = request.POST
        username = info['username']
        password = info['password']
        email = info['email']

        try:
            User.objects.create_user(username,email,password).save()
        except:
            return HttpResponse(json.dumps({'status':'error'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status':'error'}),content_type='application/json')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        info = request.POST
        username = info['username']
        password = info['password']
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request,user)
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'error'}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status':'error'}),content_type='application/json')


