from .WXBizDataCrypt import WXBizDataCrypt
import requests
import string
import random


def decrypt(*userinfo):
    # print('')
    appid, sessionkey, encrypteddata, iv = userinfo
    pc = WXBizDataCrypt(appid, sessionkey)

    return pc.decrypt(encrypteddata, iv)


def checkdata(code, ecrypteddata, iv):
    # print(code)
    # 公众号 ID
    appid = 'wx0d67af1e40427689'
    secret = 'bb6e273039f6d745c75fb6931cdd20f2'

    # 微信服务器链接
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'
    v_url = url.format(appid, secret, code)
    try:
        req = requests.get(v_url)
        res = req.json()
        print(res)
        sessionkey = res['session_key']
        openid = res['openid']

    except Exception as e:
        print('解码错误原因',e)
        data = {'error': '请求微信服务器错误'}
        return data

    # 解密用户数据
    try:
        v_res = decrypt(appid, sessionkey, ecrypteddata, iv)
        # print(v_res)

    except:
        data = {'error': '解码错误'}
        return data

    # 比较用户
    if openid != v_res['openId']:
        data = {'error': '用户认证错误'}
        return data

    cookie = gen_cookie(8)
    v_res['cookie'] = cookie

    return v_res


def gen_cookie(k):
    ascii_le = string.ascii_letters
    digits = string.digits

    str_dir = ascii_le + digits
    lst_dir = list(str_dir * 10)

    cookie = ''.join(random.sample(lst_dir,k))

    return cookie
