from compayu.models import Thought, Editor
from user.models import User
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from backsite.settings import USE_PREDICTION
import queue
import re


class thought(APIView):
    def get(self, request, format=None):
        ret = {}
        query = request.query_params.dict()
        print(query)
        if 'id' in query.keys():
            t = thought.objects.filter(id=query.get('id'))[0]
            ret['data'] = t.json()
            ret['msg'] = '下载成功'
            ret['code'] = 1
            return Response(ret)
        elif 'type_raw' in query.keys():
            thought_list = []
            thoughts = Thought.objects.filter(
                type_raw=query['type_raw']).order_by('-create_time')
            if thoughts.count() <= 0:
                return Response({'data': []})
            tail = min(int(query.get(
                'number', 1)), thoughts.count())
            tail = max(tail, 1)
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
        query = request.data
        ret = {}
        print(query)
        obj = Thought(type_raw=query['type_raw'])
        editor = Editor(content=query['content'],text=query['text'])
        editor.save()
        obj.rich_text = editor
        if 'user_id' in query:
            user = User.objects.filter(id=query['user_id'])
            if user.count()==1:
                obj.author = user[0]
        obj.save()
        ret['data'] = obj.json()
        print(ret)
        return Response(ret)

class thought_view(APIView):
    def get(self, request, format=None):
        return Response({'msg','API只支持POST方法'})
    def post(self,request, format=None):
        tid = int(request.data.get('id',-1))
        ret = {}
        if tid>=0:
            qs = Thought.objects.filter(id=tid)
            if qs.count()>0:
                t = qs[0]
                t.views += 1
                t.save()
                ret['code'] = 1
                ret['msg'] = '更新成功'
                ret['data'] = t.json()
                return Response(ret)
        ret['code'] = -1
        ret['msg'] = '更新成功'
        return Response(ret)
        



if USE_PREDICTION:
    module = None
    q = None
    worker = None
    from compayu.module import Module, check_active_worker
    module = Module("ernie_weibo4moods_finetuned", 8866)
    q = queue.Queue(1)
    q.put(module, block=True)
    worker = check_active_worker(q)
    worker.start()


class classifyText(APIView):
    def post(self, request, format=None):
        query = request.data
        global i, q
        if USE_PREDICTION:
            print(query)
            module = q.get(True)
            ret = {}
            text = query.get("text", "")
            if len(text) > 0:
                ret['data'] = module.predict([text])
                ret['code'] = 1
                ret['msg'] = '文本分类服务运行成功'
            else:
                ret['data'] = ""
                ret['code'] = -1
                ret['msg'] = '未获取到文本'
            q.put(module)
            return Response(ret)
        else:
            ret['code'] = -2
            ret['msg'] = '管理员未启用该服务'
            return Response(ret)


