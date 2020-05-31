from compayu.models import Thought
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
import json
from datetime import datetime, timedelta
from django.utils import timezone
import random
from django.views.decorators.csrf import csrf_exempt
import time
import os
from compayu.util import writeThought
from rest_framework.views import APIView
from rest_framework.response import Response
from .module import Module,check_active_worker
import time
from backsite.settings import USE_PREDICTION
import queue 
from user.md5 import md5
from user import models
from backsite.token import get_token
import re

class thought(APIView):
    def get(self, request, format=None):
        ret = {}
        query_data = request.query_params.dict()
        thought_list = []
        if 'type' in query_data:
            thoughts = Thought.objects.filter(
                type_raw=query_data['type']).order_by('-create_time')
            if thoughts.count() <= 0:
                return HttpResponse(json.dumps({'data': []}, ensure_ascii=False))
            tail = min(int(request.query_params.get('number',1)), thoughts.count())
            tail = max(tail,1)
            thoughts = thoughts[:tail]
            for item in thoughts:
                obj = item.json()
                thought_list.append(obj)
            ret['data'] = thought_list
        else:
            ret['data'] = []
            ret['msg'] = "您的输入无法识别"
        return Response(ret)
    def post(self, request, format=None):
        query_data = json.loads(request.body.decode('UTF-8'))
        print(query_data)
        obj = writeThought(query_data)
        obj.save()
        ret['data'] = obj.json()
        print(ret)
        return Response(ret)
    

class login(APIView):
    def post(self,request,format=None):
        ret = {}
        account = request.data.get("account")
        password = request.data.get("password")
        auto_login = request.data.get("auto_login")
        print(account,password,auto_login)
        logtype = ""
        user = None
        # 邮箱
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',account):
            user = models.User.objects.filter(email=account).first()
            print("邮箱登录")
            logtype = "email"
        elif re.match(r'^1[3|4|5|7|8][0-9]{9}$',account):
            user = models.User.objects.filter(email=account).first()
            logtype = "phonenum"
        else:
            ret['msg'] = "账号格式不对"
            ret['code'] = -1
            return Response(ret)
        if user:
            print("账号存在")
            # md5对照密码
            md5pwd = md5.md5(user.password)
            if password != md5pwd:
                ret["msg"] = "密码错误"
                ret['code'] = -1
                return Response(ret)
            # 将id进行加密,3600设定超时时间
            token = get_token(str(user.id), 3600)
            print("获取到token: {}".format(token))
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
            # 是否记住密码
            # 记录登录日志
            log = models.UserLoginLog(user=user, log="用户登录：登录方式 : " + logtype)
            log.save()
            # 返回token值和其他数据
            ret["msg"] = "登入成功"
            ret["token"] = token
            ret["nickname"] = user.nickname
            ret['code'] = 1
            response = Response(ret)
            age = 60*60*24*7
            if auto_login:
                if logtype=='email':
                    # 注意，因为邮箱含有特殊字符@，所以储存的cookie会带有引号，前端需要再次判定再使用
                    response.set_cookie('account', user.email, max_age=age)
                else:
                    response.set_cookie('account', user.phonenum, max_age=age)
                response.set_cookie('password_length', len(user.password), max_age=age)
                response.set_cookie('password', md5pwd, max_age=age)
            else:
                response.set_cookie('account', 'null', max_age=age)
                response.set_cookie('password_length', 0, max_age=age)
                response.set_cookie('password', 'null', max_age=age)
            return response
        print("账号不存在")
        ret['msg'] = "该账号不存在"
        ret['code'] = -1
        return Response(ret)


module = None
q = None
worker = None
if USE_PREDICTION:
    module = Module("ernie_weibo4moods_finetuned",8866)
    q = queue.Queue(1)
    q.put(module,block=True)
    worker = check_active_worker(q)
    worker.start()
class classifyText(APIView):
    def get(self, request, format=None):
        global i,q
        if USE_PREDICTION:
            module = q.get(True)
            ret = {}
            text = request.query_params.get("text", "")
            if len(text)>0:
                ret['data'] = module.predict([text])
            else:
                ret['data'] = ""
            ret['active'] = module.active
            q.put(module)
            return Response(ret)
        else:
            return Response('未启用文本分类服务')