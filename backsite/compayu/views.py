from compayu.models import Thought
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
import json
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

def thought(req):
    ret = {}
    if req.method == 'GET':
        query_data = req.GET.dict()
        thought_list = []
        if 'type' in query_data:
            thoughts = Thought.objects.filter(
                type_raw=query_data['type']).order_by('-create_time')
            if thoughts.count() <= 0:
                return HttpResponse(json.dumps({'data': []}, ensure_ascii=False))
            tail = 1
            if 'number' in query_data:
                tail = min(int(query_data['number']), thoughts.count())
            thoughts = thoughts[:tail]
            for item in thoughts:
                obj = item.json()
                thought_list.append(obj)
            ret['data'] = thought_list
        else:
            ret['data'] = '您的输入无法识别'
        res = HttpResponse(json.dumps(ret, ensure_ascii=False))
        return res
    if req.method == 'POST':
        query_data = json.loads(req.body.decode('UTF-8'))
        print(query_data)
        obj = writeThought(query_data)
        obj.save()
        ret['data'] = obj.json()
        print(ret)
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    ret['data'] = 'NONE'
    return HttpResponse(json.dumps(ret, ensure_ascii=False))

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
            text = self.request.query_params.get("text", "")
            if len(text)>0:
                ret['data'] = module.predict([text])
            else:
                ret['data'] = ""
            ret['active'] = module.active
            q.put(module)
            return Response(ret)
        else:
            return Response('未启用文本分类服务')