from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile, Goods, Directory, Log
from django.core import serializers
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .checkuser import checkdata

import requests

# 测试用
def test(request):
    return JsonResponse({'data': 'info'})

# 处理登陆
@csrf_exempt
def verify_user(request):
    if request.method == 'POST':
        # print(request.POST)
        # 初始化返回的字典
        data = {}

        # 获取小程序数据
        code = request.POST.get('code')
        encrypteddata = request.POST.get('encrypteddata')
        iv = request.POST.get('iv')

        # 检查用户
        res = checkdata(code, encrypteddata, iv)
        # print('解码信息',res)
        # 检查不通过
        errorinfo = res.get('error', None)
        if errorinfo:
            return JsonResponse(res)

        openid = res['openId']

        user = authenticate(username=openid, password=openid)
        # 登陆用户并保存 cookie
        if user:
            login(request, user)
            query_user = Profile.objects.get(openid=openid)
            query_user.cookie = res['cookie']
            query_user.save()

            # 获取用户仓库
            dir_names = []
            dirs = Directory.objects.filter(owner=query_user)
            for dir in dirs:
                dir_names.append(dir.name)
            data['dirs'] = dir_names
            data['status'] = '已登录'
        # 新建用户
        else:
            user_ins = User.objects.create_user(
                username=openid,
                password=openid
            )
            profile = Profile.objects.create(
                user=user_ins,
                openid=openid,
                cookie=res['cookie'],
                nickname=res['nickName'],
                city=res['city'],
                province=res['province'],
                gender=res['gender']

            )
            directory = Directory.objects.create(
                owner=profile,
                name='默认'
            )
            new_user = authenticate(username=openid, password=openid)
            login(request, new_user)
            data['dirs'] = ['默认']
            data['status'] = '已创建并登录'

        data['info'] = res
        # print('最终返回信息',data)

        return JsonResponse(data)

    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)


# 索引数据库
@csrf_exempt
def checkqr(request):
    # pass
    if request.method == 'POST':

        data = {}
        qrcode = request.POST.get('code')
        cookie = request.POST.get('cookie')
        dir_name = request.POST.get('dir')

        # 验证用户
        profiles = Profile.objects.filter(cookie=cookie)

        if len(profiles) != 1:
            
            data = {'error': '用户错误'}
            return JsonResponse(data)

        profile = profiles[0]

        # 获取仓库
        dirs = Directory.objects.filter(owner=profile).filter(name=dir_name)
        if len(dirs) != 1:
            data = {'error': '无此仓库，请重新登陆账户'}
            return JsonResponse(data)
        dir = dirs[0]

        # 获取商品
        goods = Goods.objects.filter(belong=dir).filter(code=qrcode)
        if len(goods) != 1:
            data = {'exist': 'none_existed'}
            return JsonResponse(data)
        good = goods[0]

        # 组装数据
        data['name'] = good.name
        data['remarks'] = good.remarks
        data['count'] = good.count

        return JsonResponse(data)


    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)


@csrf_exempt
def datain(request):

    if request.method == 'POST':

        data = {}
        qrcode = request.POST.get('code', None)
        name = request.POST.get('name', None)
        remarks = request.POST.get('remarks', None)
        cookie = request.POST.get('cookie')
        dir = request.POST.get('dir')

        # 检查用户
        profiles = Profile.objects.filter(cookie=cookie)
        if len(profiles) != 1:
            data = {'error': '用户错误'}
            return JsonResponse(data)
        profile = profiles[0]

        # 查询该用户仓库
        dirs = Directory.objects.filter(owner=profile).filter(name=dir)
        if len(dirs) != 1:
            data = {'error': '不存在此仓库'}
            return JsonResponse(data)
        dir = dirs[0]
        # 仓库使用次数加 1
        dir.freq += 1
        dir.save()

        # 筛选商品
        goods = Goods.objects.filter(belong=dir).filter(code=qrcode)
        if len(goods) == 1:
            good = goods[0]
            if name:
                good.name = name
            if remarks:
                good.remarks = remarks
            good.count += 1
            good.save()
            data['cur_count'] = good.count
            data['exist'] = 'existed'

        else:
            good = Goods.objects.create(
                belong=dir,
                name=name,
                code=qrcode,
                remarks=remarks,
                count=1
            )
            data['cur_count'] = good.count
            data['exist'] = 'newone'

        # 添加日志记录
        new_log = Log.objects.create(
            owner=profile,
            type='1',
            dir=dir,
            good=good
        )


        return JsonResponse(data)


    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)



# 商品库存状态
ENOUGH = 2
LACK = 1
RUNOUT = 0

@csrf_exempt
def dataout(request):

    if request.method == 'POST':

        # print(request.POST)
        qrcode = request.POST.get('code', None)
        cookie = request.POST.get('cookie')
        dir_name = request.POST.get('dir')

        profiles = Profile.objects.filter(cookie=cookie)
        if len(profiles) != 1:
            data = {'error': '用户错误'}
            return JsonResponse(data)
        profile = profiles[0]

        dirs = Directory.objects.filter(owner=profile).filter(name=dir_name)
        # print(dirs)
        if len(dirs) != 1:
            data = {'error': '无此仓库'}
            return JsonResponse(data)
        dir = dirs[0]
        dir.freq += 1
        dir.save()

        good = Goods.objects.filter(belong=dir).filter(code=qrcode)
        # print('dtout',good)
        data = {}
        if len(good) > 0:
            data['exist'] = 'existed'
            good = good[0]

            if good.count >= 1:
                good.count -= 1
                data['cur_count'] = good.count

            else:
                # data['cur_count'] = -1
                data['error'] = '库存不足'
                return JsonResponse(data)
            good.save()
        else:
            data['exist'] = 'noneexist'
            data['error'] = '无此商品'
            return JsonResponse(data)

        # 增加 log 记录
        new_log = Log.objects.create(
            owner=profile,
            dir=dir,
            good=good,
            type='2'
        )


        return JsonResponse(data)



    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)


@csrf_exempt
def query(request):
    # user = request.user
    if request.method == 'POST':
        data = {}
        cookie = request.POST.get('cookie')

        profiles = Profile.objects.filter(cookie=cookie)
        if len(profiles) != 1:
            data = {'error': '用户错误'}
            return JsonResponse(data)
        profile = profiles[0]

        dirs = Directory.objects.filter(owner=profile)
        count = 0
        dct_dir = {}
        for dir in dirs:
            print(dir)
            dct_goods = []
            goods = Goods.objects.filter(belong=dir)
            for good in goods:
                dct_good = {}
                dct_good['name'] = good.name
                dct_good['remark'] = good.remarks
                dct_good['count'] = good.count
                dct_good['code'] = good.code
                dct_goods.append(dct_good)

            dct_dir[dir.name] = dct_goods

        data['dirs'] = dct_dir
        # print(data)
        return JsonResponse(data)

    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)


@csrf_exempt
def builddir(request):

    if request.method == 'POST':
        data = {}
        cookie = request.POST.get('cookie')
        dirname = request.POST.get('dirname')

        profiles = Profile.objects.filter(cookie=cookie)
        if len(profiles) != 1:
            data = {'error': '用户错误'}
            return JsonResponse(data)
        profile = profiles[0]

        # 检查仓库名是否为空
        if dirname == '':
            data = {'error': '仓库名不能为空'}
            return JsonResponse(data)

        # 检查仓库是否重名
        dirs = Directory.objects.filter(owner=profile).filter(name=dirname)
        if len(dirs) > 0:
            data = {'error': '已有该仓库'}
            return JsonResponse(data)

        new_dir = Directory.objects.create(
            name=dirname,
            owner=profile,
        )

        data['status'] = '已成功建立仓库' + dirname

        # 增加日志
        new_log = Log.objects.create(
            owner=profile,
            dir=new_dir,
            type='0'
        )


        return JsonResponse(data)

    data = {'error': '仅接受POST请求'}
    return JsonResponse(data)








