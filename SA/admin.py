from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    extra = 1


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email')
        }),
    )
    inlines = (UserInfoInline,)

class FollowAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User,MyUserAdmin)
admin.site.register(Follow,FollowAdmin)

