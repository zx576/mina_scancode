from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User)

    nickname = models.CharField('微信昵称', max_length=100)
    openid = models.CharField('用户标识', max_length=100, default='default')
    cookie = models.CharField('用户认证标识', max_length=100, default='')

    GENDER = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )

    gender = models.CharField('性别', max_length=10, choices=GENDER)
    city = models.CharField('城市', max_length=100)
    province = models.CharField('省份', max_length=100)

    def __str__(self):
        return self.nickname



class Directory(models.Model):

    owner = models.ForeignKey('Profile', verbose_name='拥有者')
    name = models.CharField('仓库名', max_length=100)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_active_time = models.DateTimeField('最近操作时间', auto_now=True)

    def __str__(self):
        return self.name



class Goods(models.Model):

    belong = models.ForeignKey('Directory', verbose_name='商品归属库', default=None)
    name = models.CharField('商品名', max_length=100)
    count = models.IntegerField('数量', default=0)
    code = models.TextField('标识码')
    remarks = models.TextField('备注信息')


    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_active_time = models.DateTimeField('最近操作时间', auto_now=True)

    def __str__(self):
        return self.name
