import re
from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# 发送验证邮件
from django.core.mail import send_mail, send_mass_mail
import django.template.loader

from backsite.settings import APIKEY, APIKEYUSED
from backsite.token import get_token
from . import models
from backsite import settings
from django.utils import timezone
import random

from .md5 import md5
from .validCode.yunPian import YunPian

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions



def userPage(request):
    type = request.GET.get('type', '')
    response = render(request, 'userPage.html', {'type': 'register'})
    if type == 'register':
        # 返回登录界面
        response = render(request, 'userPage.html', {'type': 'register'})
    else:
        response = render(request, 'userPage.html', {'type': 'login'})
    return response


def userCenter(request):
    which = request.GET.get("which", '')
    response = render(request, 'userCenter.html', {'which': which})
    return response


# 用户登录接口 restful
class LoginView(APIView):
    def post(self, request):
        response = {}
        name = request.data.get("uac")
        pwd = request.data.get("upw")
        rememAC = request.data.get("rememAc")
        print(name, pwd)
        # 有可能是电话或邮箱登录
        isEmail = False
        for i in range(len(name)):
            if name[i] == '@':
                isEmail = True
                break
        if isEmail:
            user = models.User.objects.filter(email=name).first()
            logtype = "邮箱"
        else:
            user = models.User.objects.filter(phonenum=name).first()
            logtype = "电话"
        if user:
            # md5对照密码
            md5pwd = md5.md5(user.password)
            if pwd != md5pwd:
                response["msg"] = "用户名或密码错误"
                return Response(response)
            # 将id进行加密,3600设定超时时间
            token = get_token(str(user.id), 3600)
            expiration_time = datetime.now() + timedelta(hours=1, minutes=0, seconds=0)
            if models.UserToken.objects.filter(user=user).count() != 0:
                # 如果有，就更新token
                changeToken = models.UserToken.objects.filter(user=user).first()
                # 记得也要更新过期时间哦
                changeToken.expiration_time = expiration_time
                changeToken.token = token
                changeToken.save()
            else:
                # 没有该用户的token，就创建一个
                newToken = models.UserToken(user=user, token=token, expiration_time=expiration_time)
                newToken.save()
            # 更新最后登录时间
            user.lastlogin = timezone.now()
            user.save()
            # 返回token值和其他数据
            response["msg"] = "登入成功"
            response["token"] = token
            response["name"] = user.nickname
            # 是否记住密码
            ret = Response(response)
            if rememAC:
                if isEmail:
                    # 注意，因为邮箱含有特殊字符@，所以储存的cookie会带有引号，前端需要再次判定再使用
                    ret.set_cookie('uac', user.email, max_age=60*60*24*7)
                else:
                    ret.set_cookie('uac', user.phonenum, max_age=60*60*24*7)
                ret.set_cookie('upw_length', len(user.password), max_age=60 * 60 * 24 * 7)
                ret.set_cookie('upw', md5pwd, max_age=60*60*24*7)
            else:
                ret.set_cookie('uac', 'null', max_age=60 * 60 * 24 * 7)
                ret.set_cookie('upw_length', 0, max_age=60 * 60 * 24 * 7)
                ret.set_cookie('upw', 'null', max_age=60 * 60 * 24 * 7)
            # 记录登录日志
            log = models.UserLoginLog(user=user, log="用户登录：登录方式 : " + logtype)
            log.save()
            return ret
        else:
            response["msg"] = "用户名或密码错误"
            return Response(response)


def checkRegister(request):
    which = request.GET.get('with')
    # which : phone / email
    if which == 'phone':
        phone = request.POST.get('phonenum', '')
        ucode = request.POST.get('validcode', '')
        upwd = request.POST.get('pw', '')
        nickname = request.POST.get('nickname', '')
        # 检查验证码是否有效
        # 获取最新发送出去的验证码
        setcode = models.PhoneCode.objects.filter(phone=phone).order_by('-generatedate')
        # 如果找不到验证码则失败
        if setcode.count() == 0:
            return render(request, 'register.html', {'type': 'phone', 'suc': 'false', 'ret': '未检测到验证码'})
        else:
            setcode = setcode[0]
            five_minus_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 如果时间大于5分钟，则失败
            if setcode.generatedate < five_minus_ago:
                return render(request, 'register.html', {'type': 'phone', 'suc': 'false', 'ret': '验证码已过期，请重新发送'})
            # 如果不匹配则失败
            else:
                if ucode != setcode.code:
                    return render(request, 'register.html', {'type': 'phone', 'suc': 'false', 'ret': '验证码错误'})
        # 检查号码是否被注册
        count = models.User.objects.filter(phonenum=phone).count()
        if count != 0:
            return render(request, 'register.html', {'type': 'phone', 'suc': 'false', 'ret': '该号码已被注册'})
        # 保存到数据库，电话注册成功
        newuser = models.User(password=upwd, nickname=nickname, phonenum=phone, signup_type='phone', lastlogin=timezone.now(), signup_time=timezone.now())
        newuser.save()
        user = models.User.objects.filter(phonenum=phone)[0]
        # 绑定的一对一用户信息表
        userinfo = models.UserInfo(user=user, registerinfo="01")
        userinfo.save()
        return render(request, 'register.html', {'type': 'phone', 'suc': 'true', 'ret': '注册成功', 'user': user})
    elif which == 'email':
        email = request.POST.get('email', '')
        ucode = request.POST.get('validcode', '')
        upwd = request.POST.get('pw', '')
        nickname = request.POST.get('nickname', '')
        # 检查验证码是否一致
        # 获取最新发送出去的验证码
        setcode = models.EmailCode.objects.filter(email=email).order_by('-generatedate')
        if setcode.count() > 0:
            setcode = setcode[0].code
        else:
            return render(request, 'register.html', {'type': 'email', 'suc': 'false', 'ret': '未检测到验证码'})

        if setcode != ucode:
            return render(request, 'register.html', {'type': 'email', 'suc': 'false', 'ret': '验证码错误'})
        # 检查该邮箱是否已经被注册
        count = models.User.objects.filter(email=email).count()
        if count != 0:
            return render(request, 'register.html', {'type': 'email', 'suc': 'false', 'ret': '邮箱已被注册'})
        # 保存到数据库，邮箱注册成功
        newuser = models.User(password=upwd, nickname=nickname, email=email, signup_type='email', lastlogin=timezone.now(), signup_time=timezone.now())
        newuser.save()
        # 绑定的一对一用户信息表
        user = models.User.objects.filter(email=email)[0]
        userinfo = models.UserInfo(user=user, registerinfo="10")
        userinfo.save()
        return render(request, 'register.html', {'type': 'email', 'suc': 'true', 'ret': '注册成功', 'user': user})
    return HttpResponse("未知原因，注册失败")


def initEmail(request):
    email = request.POST.get('email', '')
    # 生成验证邮箱
    # 用code来验证，把这一对放进数据库中以便后面对照
    code = getEmailcode()
    emailCode = models.EmailCode(email=email, code=code)
    emailCode.save()
    link = code
    sendEmail(link, email)
    return HttpResponse("邮件已发送")


# 发送验证邮件
def sendEmail(link, aim):
    title = "空游 | Compayu 验证邮件（无需回复）"
    msg = ''
    email_from = settings.DEFAULT_FROM_EMAIL
    reciever = [
        aim
    ]
    # 加载模板
    loader = django.template.loader
    template = loader.get_template('part_email.html')
    # 渲染模板
    html_str = template.render({"link": link})
    # 发送邮件
    send_mail(title, msg, email_from, reciever, html_message=html_str)

    # 记录日志
    log = models.PhoneAndEmailLog(type='email', email=aim, log='发送邮件，验证码'+str(link))
    log.save()
    return HttpResponse("您的验证邮件已发送，请注意查收")


# 邮箱验证码
def getEmailcode():
    ret = ''
    for i in range(6):
        ret += str(random.randint(0, 9))
    return ret


# 发送验证短信
def initPhone(request):
    phone = request.POST.get('phone')
    # 手机号码正则表达式
    REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    # 检查手机号是否规范
    if not re.match(REGEX_MOBILE, phone):
        # 手机号非法
        return HttpResponse("您的手机号不合规范，请仔细核验")

    # 先检查手机号是否已经被注册过了
    if models.User.objects.filter(phonenum=phone).count() != 0:
        # 手机号已经被注册过了
        return HttpResponse("您的手机号已被注册，你可以找回密码")

    # 查看上一次这个号码发送验证码的间隔时间
    one_mintes_ago = timezone.now() - timedelta(hours=0, minutes=1, seconds=0)
    hiscode = models.PhoneCode.objects.filter(phone=phone).order_by('-generatedate')
    if hiscode.count() != 0:
        # 说明同一个电话号码已经发送过验证码
        if hiscode[0].generatedate > one_mintes_ago:
            return HttpResponse("您的发送过于频繁")

    # 生成新的code
    code = getPhonecode()
    # 把新的code数据存到数据库钟
    mycode = models.PhoneCode(phone=phone, code=code)
    mycode.save()
    response = ''
    # 发送新的验证码
    if APIKEYUSED:
        yun_pian = YunPian(APIKEY)
        response = yun_pian.send_sms(code, phone)

    # 记录日志
    log = models.PhoneAndEmailLog(type='phone', phone=phone, log=response)
    log.save()
    return HttpResponse("验证码已发送，5分钟内有效")


# 短信验证码
def getPhonecode():
    ret = ''
    for i in range(6):
        ret += str(random.randint(0, 9))
    return ret


# 登出当前账号
def logout(request):
    response = {}
    token = request.POST.get("token")
    mytoken = models.UserToken.objects.filter(token=token)[0]
    mytoken.expiration_time = datetime.now()
    mytoken.save()
    return JsonResponse(response)