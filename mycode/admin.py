from django.contrib import admin
from .models import Profile, Goods, Directory, Log

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'user', 'openid', 'gender', 'city', 'province')



@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'belong', 'code', 'count', 'remarks', 'created_time', 'last_active_time')
    # list_filter = ('belong__name',)

@admin.register(Directory)
class DirAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'freq', 'created_time', 'last_active_time')
    # list_filter = ('owner__nickname',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)
    list_filter = ('type',)
    list_display = ('owner', 'created_time', 'type', 'dir', 'good')

