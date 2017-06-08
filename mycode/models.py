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

    STATUS = (
        (1, 'LIVE'),
        (0, 'DEAD')
    )
    status = models.CharField('仓库状态', max_length=10, choices=STATUS,default=1)
    freq = models.IntegerField('使用频率', default=0)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_active_time = models.DateTimeField('最近操作时间', auto_now=True)

    def __str__(self):

        return self.name

    class meta:
        ordering = ['-freq']



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



class Log(models.Model):

    owner = models.ForeignKey('Profile', verbose_name='日志所属人', default=None)
    created_time = models.DateTimeField('日志创建时间', auto_now_add=True)
    # last_active_time = models.DateTimeField('最近操作时间', auto_now=True)

    # 日志类型
    TYPE = (
        ('0', '建库'),
        ('1', '入库'),
        ('2', '出库'),
        ('3', '删库'),
        ('4', '改库')
    )
    type = models.CharField('日志类型', max_length=10, choices=TYPE)

    # 建库
    dir = models.ForeignKey('Directory', verbose_name='所建库', blank=True, null=True)

    # 出入库
    good = models.ForeignKey('Goods', verbose_name='操作商品', blank=True, null=True)

    # def __str__(self):

        # type = ''
        # display = '用户:{0} 时间:{1} 动作:{2} 操作库:{3} 操作商品:{4}'
        # for i in self.TYPE:
        #     if self.type == i[0]:
        #         type = i[1]
        #         break
        #
        # c_time = self.created_time.strftime('%Y-%m-%d %I:%M:%S')
        #
        # g_name = ''
        # if self.good:
        #     g_name = self.good.name
        # return display.format(self.owner.nickname, c_time, type, self.dir.name, g_name)

        # return





