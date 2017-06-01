from django.contrib import admin
from .models import Profile, Goods, Directory

# Register your models here.

admin.site.register(Profile)
# class
admin.site.register(Goods)
admin.site.register(Directory)