from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    extra = 1


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'password')
    inlines = (UserInfoInline,)



admin.site.unregister(User)
admin.site.register(User,MyUserAdmin)

