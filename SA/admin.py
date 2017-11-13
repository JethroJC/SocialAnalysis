from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    filter_horizontal = ('weibo_friend','tieba_friend','zhihu_friend')
    extra = 1


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email')
        }),
    )
    inlines = (UserInfoInline,)

class WeiboAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User,MyUserAdmin)
admin.site.register(Weibo,WeiboAdmin)

