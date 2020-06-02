
import re
from user.md5 import md5
from user.models import User, UserInfo, UserLoginLog, UserToken
from backsite.token import get_token, getUserByToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta


class login(APIView):
    def get(self,request,format=None):
        return Response({'msg':'该接口不支持GET方法'})
    def post(self, request, format=None):
        ret = {}
        query = request.data
        if 'token' in query.keys():
            token = query.get('token')
            uid = getUserByToken(token)
            if uid > 0:
                ret["msg"] = "登录成功"
                ret["token"] = token
                ret['code'] = 1
                return Response(ret)
            elif uid == -1:
                ret["msg"] = "Token已过期"
                ret["token"] = "null"
                ret['code'] = -1
                return Response(ret)
            else:
                ret["msg"] = "Token错误"
                ret["token"] = "null"
                ret['code'] = -2
                return Response(ret)

        account = query.get("account")
        password = query.get("password")
        auto_login = query.get("auto_login")
        use_auto_login = query.get("use_auto_login",False)
        print(account, password, auto_login)
        logtype = ""
        user = None
        # 邮箱
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', account):
            user = User.objects.filter(email=account).first()
            print("邮箱登录")
            logtype = "email"
        elif re.match(r'^1[3|4|5|7|8][0-9]{9}$', account):
            user = User.objects.filter(email=account).first()
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
            if UserToken.objects.filter(user=user).count() != 0:
                # 如果有，就更新token
                changeToken = UserToken.objects.filter(user=user).first()
                # 记得也要更新过期时间哦
                changeToken.expiration_time = expiration_time
                changeToken.token = token
                changeToken.save()
            else:
                # 没有该用户的token，就创建一个
                newToken = UserToken(user=user, token=token,
                                     expiration_time=expiration_time)
                newToken.save()
            # 更新最后登录时间
            user.lastlogin = timezone.now()
            user.save()
            # 是否记住密码
            # 记录登录日志
            log = UserLoginLog(user=user, log="用户登录：登录方式 : " + logtype)
            log.save()
            # 返回token值和其他数据
            ret["msg"] = "登入成功"
            ret["data"] = {
                'token':token,
                'id' :user.id
            }
            ret['code'] = 1
            response = Response(ret)
            if not(use_auto_login):
                age = 60*60*24*7
                if auto_login:
                    response.set_cookie('token', token, max_age=age)
                    response.set_cookie('account', account, max_age=age)
                    response.set_cookie('password', password, max_age=age)
                    response.set_cookie('user_id',user.id,max_age=age)
                else:
                    response.set_cookie('token', 'null', max_age=age)
                    response.set_cookie('account', 'null', max_age=age)
                    response.set_cookie('password', 'null', max_age=age)
                    response.set_cookie('user_id', 'null', max_age=age)
            return response
        print("账号不存在")
        ret['msg'] = "该账号不存在"
        ret['code'] = -1
        return Response(ret)

class logout(APIView):
    def get(self,request,format=None):
        return Response({'msg':'该接口不支持GET方法'})
    def post(self,request,format=None):
        ret = {}
        # token = request.POST.get("token")
        # mytoken = UserToken.objects.filter(token=token)[0]
        # mytoken.expiration_time = datetime.now()
        # mytoken.save()
        ret['msg'] = "登出成功"
        ret['code'] = 1
        return Response(ret)