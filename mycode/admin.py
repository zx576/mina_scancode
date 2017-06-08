from django.contrib import admin
from .models import Profile, Goods, Directory, Log

# Register your models here.

admin.site.register(Profile)
# class
admin.site.register(Goods)
admin.site.register(Directory)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    # fields = ('owner', 'created_time', 'last_active_time', 'type', 'dir', 'good')

    readonly_fields = ('created_time',)
    list_filter = ('owner__nickname', 'type', 'dir__name', 'good__name')

