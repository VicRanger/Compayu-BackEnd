
from user.md5 import md5
from user.models import User, UserInfo, UserLoginLog, UserToken
from backsite.token import get_token,getUserByToken
from rest_framework.views import APIView
from rest_framework.response import Response
class user(APIView):
    def post(self, request, format=None):
        '''
        get usrinfo by token
        '''
        query = request.data
        print(query)
        uid = int(query.get('id',-1))
        if uid<0:
            token = query.get('token','')
            uid = getUserByToken(token)
        ret = {}
        if uid>0:
            data = {}
            user = User.objects.filter(id=uid)[0]
            if 'nickname' in query['query']:
                data['nickname'] = user.nickname
            if 'avatar' in query['query']:
                data['avatar'] = str(user.avatar)
            ret['data'] = data
            ret['msg'] = "查询成功"
            ret['code'] = 1
            return Response(ret)
        elif uid==-1:
            ret['msg'] = "token已过期"
            ret['code'] = -1
            return Response(ret)
        else:
            ret['msg'] = "用户不存在"
            ret['code'] = -2
            return Response(ret)
    def get(self,request,format=None):
        return Response({})